<div align="center">
  <img src="decision.png">
  <br>
</div>

# Decision Trees

The purpose of this project was to implement a decision tree learning algorithm
to predict the room in which a mobile phone was located. The dataset contains 7
Wi-Fi signal strength attributes, and the actual room location of the device. A clean
and a noisy dataset were used.

Report
------

The report describing the algorithms and metrics used can be found  <a href="Report.pdf">here</a> .

Usage
-----

To run the program:

From the ROOT directory (same as README.md):

    "python3 src/main.py"

To test with a new dataset:
1. IMPORTANT: Please place the new file inside 'src/WIFI_db/'. Otherwise it will not work.
2. Go to src/main.py
3. Go to line 53
4. Replace "noisy_file = 'src/WIFI_db/noisy_dataset.txt'"
      with "noisy_file = 'src/WIFI_db/<new_file>'"
5. To disable shuffling of the new dataset:
      - Go to line 59
      - Either delete or comment out this line
6. Run the program as instructed above
7. Performance metrics for the new dataset will be under outputs labelled with "Noisy"

NOTE: If the new dataset has under 30 samples, the program may not run, as it may not be able to split the dataset for 10-fold cross-validation.

Line 150 in src/main.py has further instrustions on how to run the visualisation.
