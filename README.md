# Energy_Disaggregation
University of Southern California DSCI 560 Group Project for Energy Disaggregation

LINK TO REDD DATASET: http://redd.csail.mit.edu/
Username: redd
Password: disaggregatetheenergy

Download low_freq.tar.bz2
Double click to uncompress and move into working pyhthon directory
Created 6 pandas dataframes for each of the 6 houses. Chose 2 appliances: lighting and washer_dryer

Resources: 
1) https://github.com/nilmtk/nilmtk
2) https://thesai.org/Downloads/Volume11No10/Paper_85-Multi_Target_Energy_Disaggregation.pdf
3) https://courses.uscden.net/d2l/le/content/20689/viewContent/344708/View?ou=20689

### Dashboard deployment
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

#### Move to directory '/Dashboard/dashboard'

###### Run `npm start` in terminal

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.


## Project Structure
```
DSCI560-Energy-Disaggregation
├─ .DS_Store
├─ .idea
│  ├─ .DS_Store
│  ├─ Energy_Disaggregation.iml
│  ├─ codeStyles
│  │  ├─ Project.xml
│  │  └─ codeStyleConfig.xml
│  ├─ inspectionProfiles
│  │  └─ profiles_settings.xml
│  ├─ jsLibraryMappings.xml
│  ├─ misc.xml
│  ├─ modules.xml
│  ├─ vcs.xml
│  └─ workspace.xml
├─ .ipynb_checkpoints
│  ├─ Energy Disaggregation CNN-checkpoint.ipynb
│  └─ Untitled-checkpoint.ipynb
├─ CSCI560
│  ├─ .DS_Store
│  ├─ Energy_Disaggregation
│  │  ├─ .DS_Store
│  │  ├─ .ipynb_checkpoints
│  │  │  ├─ Energy_Disaggregation_NN-checkpoint.ipynb
│  │  │  └─ Energy_Disaggregation_SVM-checkpoint.ipynb
│  │  ├─ CNN.py
│  │  ├─ Energy_Disaggregation_NN.ipynb
│  │  ├─ Energy_Disaggregation_SVM.ipynb
│  │  ├─ Event_Detection.py
│  │  ├─ README.md
│  │  ├─ __pycache__
│  │  │  ├─ Event_Detection.cpython-37.pyc
│  │  │  ├─ Event_Detection.cpython-38.pyc
│  │  │  ├─ preprocess.cpython-37.pyc
│  │  │  └─ preprocess.cpython-38.pyc
│  │  ├─ preprocess.py
│  │  ├─ requirements.txt
│  │  ├─ test_windows_15.pkl
│  │  └─ windows_15.pkl
│  └─ low_freq.tar.bz2
├─ Dashboard
│  ├─ .DS_Store
│  ├─ .idea
│  │  ├─ .DS_Store
│  │  ├─ codeStyles
│  │  │  ├─ Project.xml
│  │  │  └─ codeStyleConfig.xml
│  │  ├─ inspectionProfiles
│  │  │  └─ Project_Default.xml
│  │  ├─ misc.xml
│  │  ├─ modules.xml
│  │  ├─ vcs.xml
│  │  └─ workspace.xml
│  ├─ Dashboard.iml
│  ├─ Untitled-1.psd
│  ├─ dashboard
│  │  ├─ .DS_Store
│  │  ├─ README.md
│  │  ├─ package-lock.json
│  │  ├─ package.json
│  │  ├─ public
│  │  │  ├─ favicon.ico
│  │  │  ├─ index.html
│  │  │  ├─ logo192.png
│  │  │  ├─ logo512.png
│  │  │  ├─ manifest.json
│  │  │  └─ robots.txt
│  │  └─ src
│  │     ├─ .DS_Store
│  │     ├─ App.css
│  │     ├─ App.js
│  │     ├─ charts
│  │     │  ├─ appliances
│  │     │  │  ├─ Appliances.js
│  │     │  │  └─ PieChart.js
│  │     │  ├─ daily
│  │     │  │  ├─ AreaChart.js
│  │     │  │  ├─ Daily.css
│  │     │  │  ├─ Daily.js
│  │     │  │  └─ daily-usage.json
│  │     │  ├─ data
│  │     │  │  ├─ nn_appliances.json
│  │     │  │  ├─ nn_houses.json
│  │     │  │  └─ svm_results.json
│  │     │  └─ neighbors
│  │     │     ├─ BarChart.js
│  │     │     ├─ Neighbors.css
│  │     │     ├─ Neighbors.js
│  │     │     └─ data-neighbor.json
│  │     ├─ energy-logo.svg
│  │     ├─ index.css
│  │     ├─ index.js
│  │     ├─ logo.png
│  │     ├─ logo.svg
│  │     └─ other
│  │        ├─ .DS_Store
│  │        ├─ app-info
│  │        │  ├─ ApplianceInfo.css
│  │        │  ├─ ApplianceInfo.js
│  │        │  └─ light.png
│  │        └─ user-info
│  │           ├─ UserInfo.css
│  │           ├─ UserInfo.js
│  │           ├─ user.jpeg
│  │           ├─ user.jpg
│  │           └─ user.png
│  └─ data-manipulation
│     └─ clean-save-result.py
├─ Energy Disaggregation CNN.ipynb
├─ Event_Detection.py
├─ LICENSE
├─ README.md
├─ Regression_Tree.py
├─ __pycache__
├─ comparing_nilm_algorithms.ipynb
├─ low_freq
│  ├─ .DS_Store
│  ├─ house_1
│  │  ├─ channel_1.dat
│  │  ├─ channel_10.dat
│  │  ├─ channel_11.dat
│  │  ├─ channel_12.dat
│  │  ├─ channel_13.dat
│  │  ├─ channel_14.dat
│  │  ├─ channel_15.dat
│  │  ├─ channel_16.dat
│  │  ├─ channel_17.dat
│  │  ├─ channel_18.dat
│  │  ├─ channel_19.dat
│  │  ├─ channel_2.dat
│  │  ├─ channel_20.dat
│  │  ├─ channel_3.dat
│  │  ├─ channel_4.dat
│  │  ├─ channel_5.dat
│  │  ├─ channel_6.dat
│  │  ├─ channel_7.dat
│  │  ├─ channel_8.dat
│  │  ├─ channel_9.dat
│  │  └─ labels.dat
│  ├─ house_2
│  │  ├─ channel_1.dat
│  │  ├─ channel_10.dat
│  │  ├─ channel_11.dat
│  │  ├─ channel_2.dat
│  │  ├─ channel_3.dat
│  │  ├─ channel_4.dat
│  │  ├─ channel_5.dat
│  │  ├─ channel_6.dat
│  │  ├─ channel_7.dat
│  │  ├─ channel_8.dat
│  │  ├─ channel_9.dat
│  │  └─ labels.dat
│  ├─ house_3
│  │  ├─ channel_1.dat
│  │  ├─ channel_10.dat
│  │  ├─ channel_11.dat
│  │  ├─ channel_12.dat
│  │  ├─ channel_13.dat
│  │  ├─ channel_14.dat
│  │  ├─ channel_15.dat
│  │  ├─ channel_16.dat
│  │  ├─ channel_17.dat
│  │  ├─ channel_18.dat
│  │  ├─ channel_19.dat
│  │  ├─ channel_2.dat
│  │  ├─ channel_20.dat
│  │  ├─ channel_21.dat
│  │  ├─ channel_22.dat
│  │  ├─ channel_3.dat
│  │  ├─ channel_4.dat
│  │  ├─ channel_5.dat
│  │  ├─ channel_6.dat
│  │  ├─ channel_7.dat
│  │  ├─ channel_8.dat
│  │  ├─ channel_9.dat
│  │  └─ labels.dat
│  ├─ house_4
│  │  ├─ channel_1.dat
│  │  ├─ channel_10.dat
│  │  ├─ channel_11.dat
│  │  ├─ channel_12.dat
│  │  ├─ channel_13.dat
│  │  ├─ channel_14.dat
│  │  ├─ channel_15.dat
│  │  ├─ channel_16.dat
│  │  ├─ channel_17.dat
│  │  ├─ channel_18.dat
│  │  ├─ channel_19.dat
│  │  ├─ channel_2.dat
│  │  ├─ channel_20.dat
│  │  ├─ channel_3.dat
│  │  ├─ channel_4.dat
│  │  ├─ channel_5.dat
│  │  ├─ channel_6.dat
│  │  ├─ channel_7.dat
│  │  ├─ channel_8.dat
│  │  ├─ channel_9.dat
│  │  └─ labels.dat
│  ├─ house_5
│  │  ├─ channel_1.dat
│  │  ├─ channel_10.dat
│  │  ├─ channel_11.dat
│  │  ├─ channel_12.dat
│  │  ├─ channel_13.dat
│  │  ├─ channel_14.dat
│  │  ├─ channel_15.dat
│  │  ├─ channel_16.dat
│  │  ├─ channel_17.dat
│  │  ├─ channel_18.dat
│  │  ├─ channel_19.dat
│  │  ├─ channel_2.dat
│  │  ├─ channel_20.dat
│  │  ├─ channel_21.dat
│  │  ├─ channel_22.dat
│  │  ├─ channel_23.dat
│  │  ├─ channel_24.dat
│  │  ├─ channel_25.dat
│  │  ├─ channel_26.dat
│  │  ├─ channel_3.dat
│  │  ├─ channel_4.dat
│  │  ├─ channel_5.dat
│  │  ├─ channel_6.dat
│  │  ├─ channel_7.dat
│  │  ├─ channel_8.dat
│  │  ├─ channel_9.dat
│  │  └─ labels.dat
│  └─ house_6
│     ├─ channel_1.dat
│     ├─ channel_10.dat
│     ├─ channel_11.dat
│     ├─ channel_12.dat
│     ├─ channel_13.dat
│     ├─ channel_14.dat
│     ├─ channel_15.dat
│     ├─ channel_16.dat
│     ├─ channel_17.dat
│     ├─ channel_2.dat
│     ├─ channel_3.dat
│     ├─ channel_4.dat
│     ├─ channel_5.dat
│     ├─ channel_6.dat
│     ├─ channel_7.dat
│     ├─ channel_8.dat
│     ├─ channel_9.dat
│     └─ labels.dat
├─ neural_network.py
├─ pkl_files
│  ├─ house_1.csv
│  ├─ house_1.pkl
│  ├─ house_2.csv
│  ├─ house_2.pkl
│  ├─ house_3.csv
│  ├─ house_3.pkl
│  ├─ house_4.csv
│  ├─ house_4.pkl
│  ├─ house_5.pkl
│  ├─ house_6.pkl
│  ├─ svm_result_windows_lighting.pkl
│  ├─ svm_result_windows_washer_dryer.pkl
│  ├─ test_windows.pkl
│  └─ windows.pkl
├─ pkl_results
│  ├─ nn_predict_house_5_kitchen_outlets.pkl
│  ├─ nn_predict_house_5_lighting.pkl
│  ├─ nn_predict_house_5_washer_dryer.pkl
│  ├─ nn_predict_house_6_kitchen_outlets.pkl
│  ├─ nn_predict_house_6_lighting.pkl
│  ├─ nn_predict_house_6_stove.pkl
│  ├─ nn_predict_house_6_washer_dryer.pkl
│  ├─ svm_result_windows_lighting.pkl
│  └─ svm_result_windows_washer_dryer.pkl
├─ preprocess.py
└─ src

```