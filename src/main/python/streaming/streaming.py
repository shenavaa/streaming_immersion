from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kinesis import KinesisUtils, InitialPositionInStream
# Set up the Spark context and streaming context
conf = SparkConf()
conf.setAppName("KinesisStreaming")
sc = SparkContext.getOrCreate(conf)
ssc = StreamingContext(sc, 10)  # Batch interval of 10 seconds
# Kinesis stream parameters
kinesisStreamName = "bus-tracking"
kinesisRegion = "us-east-1"
kinesisEndpointUrl = "https://kinesis.us-east-1.amazonaws.com"
kinesisAppName = "KinesisStreaming"
# Create a Kinesis stream DStream
kinesisStream = KinesisUtils.createStream(
    ssc,
    kinesisAppName,
    kinesisStreamName,
    kinesisEndpointUrl,
    kinesisRegion,
    InitialPositionInStream.TRIM_HORIZON,
    2  # Storage level
)
# Process the data in the stream
kinesisStream.map(lambda x: x).pprint()
# Start the streaming context
ssc.start()
#ssc.awaitTermination()

