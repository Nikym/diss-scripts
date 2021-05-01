# FAT Tests
echo "Running FAT 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
cp /home/nikita/diss/PoseCNN/output/fat/lov_train/fat_0008\(13\)/val.txt /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
split -l 4000 /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaa /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xab /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xac /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xad /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xae /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s

# FAT no-kitedemo
echo "Running FAT w/o kitedemo 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
cp /home/nikita/diss/PoseCNN/output/fat/lov_train/fat_nok_0008\(16\)/val.txt /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
split -l 4000 /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaa /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xab /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xac /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xad /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s

# Mixed
echo "Running Mixed 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/fat/output /home/nikita/diss/PoseCNN/data/LOV/data
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
cp /home/nikita/diss/PoseCNN/output/fat/lov_train/mixed_0008\(19\)/val.txt /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
split -l 4000 /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaa /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xab /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xac /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xad /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xae /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaf /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s

# Custom Noisy
echo "Running Custom Noisy 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/generated_data/processed2 /home/nikita/diss/PoseCNN/data/LOV/data
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
cp /home/nikita/diss/PoseCNN/output/fat/lov_train/noisy_0008\(10\)/val.txt /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
split -l 4000 /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaa /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xab /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xac /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xad /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xae /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xaf /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xag /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
rm /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
mv /home/nikita/diss/PoseCNN/data/LOV/xah /home/nikita/diss/PoseCNN/data/LOV/keyframe.txt
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s
echo "COMPLETE"