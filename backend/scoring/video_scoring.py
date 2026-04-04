import os
import json

class video_scoring:

    def majority(self,video_name):
        label_count = {}

        file_path = os.path.join("..","outputs",video_name,"frame_ranked.json")
        with open(file_path,"r") as file:

            data = json.load(file)
                
            ranked_frames = data.get('ranked_frames')
            for frame in ranked_frames:
                label = frame.get('label')

                if label in label_count:
                    label_count[label] += 1
                else:
                    label_count[label] = 1

        top_label = max(label_count, key=label_count.get)

        return label_count,top_label
            
    def average_confidence(self,video_name):

        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_dir = os.path.join(backend_dir,"outputs", video_name)

        file_path = os.path.join(video_dir,"frame_ranked.json")

        label_sum = {}
        label_count = {}

        with open(file_path,"r") as file:

            data = json.load(file)

            ranked_frames = data.get('ranked_frames')

            for frame in ranked_frames:
                label = frame.get('label')
                confidence = frame.get('confidence')

                if label is None or confidence is None:
                    continue

                if label in label_sum:
                    label_sum[label] += confidence
                    label_count[label] += 1
                else:
                    label_sum[label] = confidence
                    label_count[label] = 1


        label_avg ={}

        for label in label_sum:
            label_avg[label] = label_sum[label]/label_count[label]

        top_label = max(label_avg, key=label_avg.get)
        top_conf = label_avg[top_label]

        return top_label,top_conf
        
