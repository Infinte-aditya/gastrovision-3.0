import os
import ffmpeg

def extract_frames(input_file, output_dir):

    if not (os.path.exists(output_dir)):
        os.makedirs(output_dir)

    try:
        {
            ffmpeg
            .input(input_file)
            .output(os.path.join(output_dir, 'frame_%04d.jpg'), format  = 'image2')
            .run(capture_stdout=True, capture_stderr=True)
        }


        print(f"extraction completed saved in {output_dir}")
    except ffmpeg.Error as e:
        print(f"error is {e}")

def find_metadata(input_file):

    probe = ffmpeg.probe(input_file)
    
    #print(probe)
    print("duration: ",probe['format']['duration'])
    print("number of frames: ",probe['streams'][0]['nb_frames'])

if __name__ == "__main__":
    #extract_frames("ample_video.mp4",'output_videos')
    find_metadata("ample_video.mp4")
