import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reading the dataset contents as Storing in a variable data which stores the data as DataFrame
# The Dataset is Download from the uci machine learning repository

data = pd.read_csv("dataset.csv")
# The Below Two Lines are to Observe the data to check details about the dataset we imported
print(data.describe())
print(data.info())


# We need to check for outliers in the data using a scatter_plot or box_plot method.
# So that we can identify and remove those outliers to increase our model efficiency.

from pandas.plotting import scatter_matrix
scatter_matrix(data[['MEDV', 'RM', 'LSTAT', 'ZN']], figsize=(12, 8))
plt.show()

# I plotted only for the strongly correlated attributes.
# By observing the plots for the attributes we can identify the outliers in the dataset.
# Now we will remove the outliers using the Quantile Based Flooring and Capping method.

# This Method is used to remove the outliers
def quantify(attribute):
    lower_bound = data[attribute].quantile(0.10)
    upper_bound = data[attribute].quantile(0.90)
    data[attribute] = np.where(data[attribute] < lower_bound, lower_bound, data[attribute])
    data[attribute] = np.where(data[attribute] > upper_bound, upper_bound, data[attribute])


# Now we are going to quantify all the attributes except MEDV and CHAS
att = data.columns.drop(['MEDV', 'CHAS'])  # This drop is not going to effect the original dataset
for i in att:
    quantify(i)


# Train-Test Split
# Now we will split the dataset into training-set and testing-set
# We will be using the training-set to train our ML model
# Then we test our Model's Accuracy by using the test-set

print(data['CHAS'].value_counts())

# After Executing the above line we can observe that there are only 2 values that CHAS attribute can have
# Either 0 or 1 so we need to divide the dataset in such a way that both the train-set and test-set
# contain minimum number of 1's and 0's so that our model can identify that CHAS can hold values 0 or 1
# It is Crucial to do that step because it can effect our model's Accuracy in predicting
# So do the above step we use a predefined function in SK-Learn module called as StratifiedShuffleSplit()

# Splitting the data into 80:20 ratio where training set is of 80%(0.8) of data and test set is of 20%(0.2) of data.
from sklearn.model_selection import StratifiedShuffleSplit
shuffle_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in shuffle_split.split(data, data['CHAS']):
    Train_Set = data.loc[train_index]
    Test_Set = data.loc[test_index]

print(Train_Set['CHAS'].value_counts())
print(Test_Set['CHAS'].value_counts())
# After Executing the Above Two Print statements we can observe that both datasets are filled with certain amount
# of 1's and 0's for the attribute CHAS

# Now we need to check the relationship among the other attributes and the final attribute( MEDV )

corr_matrix = Train_Set.corr()
print(corr_matrix['MEDV'].sort_values(ascending=False))

# We need to check the correlation between the Main attribute with other attributes because it helps us understand
# the data more and we can remove few attributes if they are weakly correlated.
# For Example in our dataset few of the weakly correlated attributes are CHAS and DIS.
# But I am not removing them in this Model but it is good to remove few attributes to increase our Accuracy.

# Not only weakly correlated but we can also observe the strongly related attributes which help us collect useful
# data which should definitely contain the strongly correlated attribute values and mostly we need take care that
# these attributes don't have null attributes and if at all there are null values we need to process the data.


Train_Labels = Train_Set['MEDV'].copy()  # We store the Final Attribute in this variable
Train_Set.drop('MEDV', axis=1, inplace=True)
# We are going to remove the final attribute that needs to be predicted

# We need to check if there are any null values in our dataset so that we can preprocess the data and replace
# the null values with mean or median to prevent those null values from hampering our Ml Model.
# We are also going to standardize our data so that it won't be biased in predicting data.
# To do both of the tasks we are going to use predefined functions in sklearn module
# PipeLine helps us in performing both the tasks one after other by passing one function or process output as
# input to other function or process


from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

my_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')), ('std_scalar', StandardScaler())])
Train_Set = my_pipeline.fit_transform(Train_Set)
# Remember that the above data is a numpy array and not a dataframe

# Finally Selecting a Regression Model for our ML Model
# I Chose RandomForest even when linear model got less error because if at all the dataset increases
# The error done by linear model may increase to a greater extent than that of Random Forest.

# from sklearn.linear_model import LinearRegression
# model = LinearRegression()

# from sklearn.tree import DecisionTreeRegressor
# model = DecisionTreeRegressor()

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()

model.fit(Train_Set, Train_Labels)
predicted_data_Train = model.predict(Train_Set)

# We Trained our model with the training set now we need test it on the test-set
Test_Labels = Test_Set['MEDV'].copy()
Test_Set.drop('MEDV', axis=1, inplace=True)
Test_Set = my_pipeline.fit_transform(Test_Set)
predicted_data_Test = model.predict(Test_Set)

# Calculating Root Mean Squared error
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(Test_Labels, predicted_data_Test)
root_mse = np.sqrt(mse)
print("Root Mean Squared Error =", root_mse)
# The Above Tells us the error that our model is making while predicting
