g++ -I/usr/local/include/opencv -I/usr/local/include/opencv2 -L/usr/local/lib/ -g -o boneCpp  boneCpp.cpp -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_ml -lopencv_video -lopencv_features2d -lopencv_calib3d -lopencv_objdetect -lopencv_stitching -lopencv_imgcodecs -lopencv_videoio
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export LD_LIBRARY_PATH
