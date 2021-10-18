# data analysis and wrangling
import pandas as pd


import streamlit as st

# Random Forest
from sklearn.ensemble import RandomForestClassifier

#データ整理
train_df = pd.read_csv('/Users/hayato/streamlit/Titanic/train_df.csv')
train_df = train_df.drop(['Unnamed: 0'], axis=1)

X_train = train_df.drop("Survived", axis=1)
Y_train = train_df["Survived"]

# Random Forest
random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)


#テストデータの整理、モデルの実行
test_df = pd.read_csv('/Users/hayato/streamlit/Titanic/test_df.csv')
test_df = test_df.drop(['Unnamed: 0'], axis=1)
X_test = test_df
Y_pred = random_forest.predict(X_test)


#StreamLit関連
st.title('あなたのタイタニック生存予想')

st.sidebar.write(f"""
## 質問に答えてください
""")

#質問項目から導く変数
Pclass = st.sidebar.slider('年収（万円）',0,4000,300)
Sex = st.sidebar.selectbox('性別',('男性','女性'))
Age = st.sidebar.selectbox('年齢', ('１６歳未満', '１６歳以上３２歳未満', '３２歳以上４８歳未満','４８歳以上６４歳未満','６４歳以上'))
IsAlone = st.sidebar.selectbox('所帯',('独身（子無し）','所帯あり（子持ちも）'))


#Sexの数値化
if Sex == '男性':
    Sex = 1
else:
    Sex = 0

#IsAloneの数値化
if IsAlone == '独身（子無し）':
    IsAlone = 1
else:
    IsAlone = 0


#Ageの変数化
if Age == '１６歳未満':
    Age = 0
elif Age == '１６歳以上３２歳未満':
    Age = 1
elif Age == '３２歳以上４８歳未満':
    Age = 2
elif Age == '４８歳以上６４歳未満':
    Age = 3
elif Age == '６４歳以上':
    Age = 75


#Titleの判定
if Sex == 1:
    Title = 1
if Sex == 0 & IsAlone == 0:
    Title = 3
if Sex == 0 & IsAlone == 1:
    Title = 2

#Pclassを判定、変数化
if Pclass >= 3001:
    Pclass = 1
elif Pclass <= 600:
    Pclass = 3
elif Pclass > 600 & Pclass < 3000:
    Pclass = 2


#Fareの判定、変数化
if Pclass == 1:
    Fare = 3
elif Pclass == 2:
    Fare = 2
else :
    Fare = 0

#AgeClassのアルゴリズム
AgeClass = Age * Pclass

#出港地は面倒臭いので固定
Embarked = 1

question_df = pd.DataFrame({
    'Pclass'    :[Pclass],	
    'Sex'	    :[Sex],
    'Age'	    :[Age],
    'Fare'      :[Fare],	
    'Embarked'  :[Embarked],	
    'Title'	    :[Title],
    'IsAlone'	:[IsAlone],
    'AgeClass'  :[AgeClass]
})



#ランダムフォレストを実行
pred = random_forest.predict(question_df)

#一応質問結果を表示
st.table(question_df)

if pred[0] == 1:
    st.write(f"""
## あなたは生き残るでしょう
""")
else:
    st.write(f"""
## あなたは死にます…
""")
