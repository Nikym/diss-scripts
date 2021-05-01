KEYFRAME_PATH = "/home/nikita/diss/PoseCNN/data/LOV/"
# FAT Tests
echo "Running FAT 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm $KEYFRAME_PATH"keyframe.txt"
cp /home/nikita/diss/PoseCNN/outputs/fat/lov_train/fat_0008\(13\)/val.txt $KEYFRAME_PATH"keyframe.txt"
split -l 4000 $KEYFRAME_PATH"keyframe.txt"
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaa" $KEYFRAME_PATH"keyframe.txt"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xab" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xac" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xad" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xae" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s

# FAT no-kitedemo
echo "Running FAT w/o kitedemo 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm $KEYFRAME_PATH"keyframe.txt"
cp /home/nikita/diss/PoseCNN/outputs/fat/lov_train/fat_nok_0008\(16\)/val.txt $KEYFRAME_PATH"keyframe.txt"
split -l 4000 $KEYFRAME_PATH"keyframe.txt"
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaa" $KEYFRAME_PATH"keyframe.txt"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xab" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xac" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xad" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s

# Mixed
echo "Running Mixed 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm $KEYFRAME_PATH"keyframe.txt"
cp /home/nikita/diss/PoseCNN/outputs/fat/lov_train/mixed_0008\(19\)/val.txt $KEYFRAME_PATH"keyframe.txt"
split -l 4000 $KEYFRAME_PATH"keyframe.txt"
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaa" $KEYFRAME_PATH"keyframe.txt"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xab" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xac" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xad" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xae" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaf" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s

# Custom Noisy
echo "Running Custom Noisy 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/generated_data/processed2 /home/nikita/diss/PoseCNN/data/LOV/data
rm $KEYFRAME_PATH"keyframe.txt"
cp /home/nikita/diss/PoseCNN/outputs/fat/lov_train/noisy_0008\(10\)/val.txt $KEYFRAME_PATH"keyframe.txt"
split -l 4000 $KEYFRAME_PATH"keyframe.txt"
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaa" $KEYFRAME_PATH"keyframe.txt"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xab" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xac" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xad" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xae" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xaf" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xag" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm $KEYFRAME_PATH"keyframe.txt"
mv $KEYFRAME_PATH"xah" $KEYFRAME_PATH"keyframe.txt"
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
echo "COMPLETE"