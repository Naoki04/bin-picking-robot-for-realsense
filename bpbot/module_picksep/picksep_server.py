import os
import time
import grpc
from concurrent import futures
from tangle import Config, Inference
from tangle.utils import angle2vector 
import numpy as np
import picksep_pb2 as psmsg
import picksep_pb2_grpc as psrpc

class PickSepServer(psrpc.PickSepServicer): 
    def initialize(self):        
        # create config for the server
        config_data = {
            "root_dir_win": "C:\\Users\\xinyi\\Documents",
            "root_dir_linux": "/home/hlab/Documents/",
            "infer": 
            {
                "net_type": "pick_sep",
                "backbone": "resnet50",
                "sep_type": "spatial", 
                "mode": "test",
                "use_cuda": True,
                "batch_size": 1,
                "img_height": 512,
                "img_width": 512,
                "pick_ckpt_folder": ["try8","model_epoch_10.pth"],
                # "pick_ckpt_folder": ["try8","model_epoch_10.pth"],
                # "sepp_ckpt_folder": ["try_38","model_epoch_4.pth"],
                # "sepd_ckpt_folder": ["try_sepnet_d_vector_eight","model_epoch_20.pth"]
                "sepp_ckpt_folder": ["try_refine","model_epoch_19.pth"],
                # "sepd_ckpt_folder_s": ["try_action_map","model_epoch_68.pth"]
                # "sepd_ckpt_folder_s": ["try_action_map_augment","model_epoch_29.pth"]
                "sepd_ckpt_folder_s": ["try_action_map_augment_add","model_epoch_40.pth"]
                # "sepd_ckpt_folder_s": ["try_action_map_augment","model_epoch_35.pth"]
            }
        }
        
        cfg = Config(config_type="infer", config_data=config_data)
        self.inference = Inference(config=cfg)
     
    def infer_picknet(self, request, context): 
        """
        Returns:
            array (5): [pickorsep, x, y score * 2]
        """
        ret = self.inference.infer(data_dir=request.imgpath, net_type="pick")
        pickorsep = ret[0][0]
        pn_points = ret[1][0]
        pn_scores = ret[2][0]

        l = np.concatenate([[pickorsep], pn_points[pickorsep], pn_scores]) 
        l2bytes = np.ndarray.tobytes(l)

        return psmsg.Ret(ret=l2bytes)

    def infer_sepnet(self, resquest, context):
        """
        Returns:
            array (6+#directions): [pull x,y, hold x,y, vector x,y + score * #directions]
        """
        ret = self.inference.infer(data_dir=resquest.imgpath, net_type="sep")
        snp_points = ret[0][0]
        snd_vector = ret[1][0]
        snd_scores = ret[2][0]
        # snd_scores = np.array(ret[1][0])
        # vector_idx = np.argmax(snd_scores)
        
        # vector = angle2vector(vector_idx * 360 / len(snd_scores))
        l = np.concatenate([snp_points.ravel(), snd_vector.ravel(), snd_scores.ravel()])
         
        l2bytes = np.ndarray.tobytes(l)
        return psmsg.Ret(ret=l2bytes)

def serve(host="localhost:50050"):
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24
    options = [('grpc.max_message_length', 100 * 1024 * 1024)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = options)
    psserver = PickSepServer()
    m = psserver.initialize()
    psrpc.add_PickSepServicer_to_server(psserver, server)
    server.add_insecure_port(host)
    server.start()
    print("[*] PickNet + SepNet server is started!")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0) 

if __name__ == "__main__":
    serve(host="localhost:50050")