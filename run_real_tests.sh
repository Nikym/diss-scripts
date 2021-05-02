# FAT Tests
echo "Running FAT 0.0008 tests"
rm /home/nikita/diss/PoseCNN/data/LOV/data
ln -s /media/nikita/Samsung_T5/diss/ycb/YCB_dataset/data /home/nikita/diss/PoseCNN/data/LOV/data
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat.sh 0
sleep 10s

# FAT no-kitedemo
echo "Running FAT w/o kitedemo 0.0008 tests"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_fat_nok.sh 0
sleep 10s

# Mixed
echo "Running Mixed 0.0008 tests"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_mixed.sh 0
sleep 10s

# Custom Noisy
echo "Running Custom Noisy 0.0008 tests"
rm -r /home/nikita/diss/PoseCNN/data/cache
cd /home/nikita/diss/PoseCNN
./experiments/scripts/fat_data_test_noisy.sh 0
sleep 10s

echo "COMPLETE"