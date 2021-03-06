# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 17:17:44 2021
rlmlrml
@author: devansh
"""
# importing all essential libraries
import keras
from keras.optimizers import SGD
from keras.datasets import mnist
from keras.models import Sequential,load_model
from keras.layers import Dense,Flatten,Dropout
from keras.layers import MaxPooling2D,Conv2D
import numpy as np
import cv2

#load mnist data into train and test sets
(x_train,y_train),(x_test,y_test)=mnist.load_data()

#find image rows and columns of training image
#with indent 0 being row and indent 1 being column
img_rows=x_train[0].shape[0]
img_cols=x_train[0].shape[1]

#reshape x_train and x_test data into 4 dimnension by adding 1 as 4th dimension
x_train=x_train.reshape(x_train.shape[0],img_rows,img_cols,1)
x_test=x_test.reshape(x_test.shape[0],img_rows,img_cols,1)
print(x_train.shape)  #print to check if dimension changes or not 


#change the dimension of input source also
input_shape=(img_rows,img_cols,1)

#convert x_train and x_test to float values

x_train=x_train.astype('float32')
x_test=x_test.astype('float32')

#normalize the values of x_train and x_test by diving it with 255
#(as 255 is the highest value) to get the dataset in range of 0 and 1

x_train /= 255
x_test /= 255

#convert y_test and y_train into categorical data using hot encoder

from keras.utils import np_utils
y_train=np_utils.to_categorical(y_train)
y_test=np_utils.to_categorical(y_test)

num_classes=y_test.shape[1]

#Building CNN model

model=Sequential()
model.add(Conv2D(32, (2,2),
                 activation='relu',
                 input_shape=input_shape))
model.add(Conv2D(64, (2,2), 
                 activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Dropout(0.25 ))

model.add(Flatten())

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(num_classes,activation='softmax'))

model.compile(loss = 'categorical_crossentropy',
              optimizer = SGD(0.01),
              metrics = ['accuracy'])

print(model.summary())

#training our model with suitable epochs and batch number

batch_number=34
epochs=12

model.fit(x_train,y_train,
          batch_size=batch_number,
          epochs=epochs,verbose=1,
          validation_data=(x_test,y_test))
score=model.evaluate(x_test,y_test,verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#save your model to your required location
model.save("C:/Users/devansh/Desktop/projects/handwritten Digit Recognition/handwritten Digit Recognition.h5")
print("model saved successfully")

# to load the model just type load_model then its path
classifier=load_model("C:/Users/devansh/Desktop/projects/handwritten Digit Recognition/handwritten Digit Recognition.h5")

#testing our model on some random digits
#%%
def data_test(name,pred,image):
    
    BLACK=[0,0,0]
    expanded_image=cv2.copyMakeBorder(image, 0, 0, 0, resize_img.shape[0], cv2.BORDER_CONSTANT,value=BLACK)
    expanded_image=cv2.cvtColor(expanded_image,cv2.COLOR_GRAY2BGR)
    cv2.putText(expanded_image,str(pred),(152,72),cv2.FONT_ITALIC,3,(0,255,0),2)
    cv2.imshow(name,expanded_image)
    
for i in range(0,15):
    rand_img=np.random.randint(0,len(x_test))
    image=x_test[rand_img]
    resize_img=cv2.resize(image, None,fx=4,fy=4,interpolation=cv2.INTER_CUBIC)
    image=image.reshape(1,28,28,1)
    res = str(classifier.predict_classes(image, 1, verbose = 0)[0])
    
    data_test("predictions", res, resize_img)
    cv2.waitKey()
    
cv2.destroyAllWindows()
    

#
