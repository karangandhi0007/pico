import sys
import time
import cv2
# from picamera.array import PiRGBArray
# from picamera import PiCamera
from kafka import KafkaProducer
from kafka.errors import KafkaError

topic = "testpico"

def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic. 
    Kafka Server is expected to be running on the localhost. Not partitioned.
    
    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-brokers:9092', batch_size=8192, linger_ms=0, acks=0, retries=0, buffer_memory=3096000000, send_buffer_bytes=100000000, receive_buffer_bytes=100000000)

    # Open file
    video = cv2.VideoCapture(video_file)
    video.set(cv2.CAP_PROP_FRAME_WIDTH,3840)

    video.set(cv2.CAP_PROP_FRAME_HEIGHT,2160)

    video.set(cv2.CAP_PROP_FPS,60)
    
    print('publishing video...')

    while(video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())

        time.sleep(0.04)
    video.release()
    print('publish complete')

    
def publish_camera():
    """
    Publish camera video stream to specified Kafka topic.
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='my-cluster-kafka-brokers:9092')

    
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
        
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())
            image.write(buffer.tobytes())
    
    
            # Choppier stream, reduced load on processor
            time.sleep(0.04)
            
    except:
        print("\nExiting.")
        sys.exit(1)

    
    camera.release()

	
	
publish_video('Countdown1.mp4')
