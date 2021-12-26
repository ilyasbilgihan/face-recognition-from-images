import face_recognition
import pickle
import cv2
import os
from sklearn import svm


def face_recognize(location):


    examples = os.listdir(location)
    
    #trained data
    data = pickle.load(open('./trained/data.sav', 'rb'))
    encodings = []
    names = []
    for person in data:
        for enc in data[person]:
            encodings.append(enc)
            names.append(person)
    
    clf = svm.SVC(gamma='scale')
    clf.fit(encodings,names)
    
    
    for example in examples:
        
        img = cv2.imread(location + example)
        
        width = 400
        ratio = width / img.shape[1]
        height = int(img.shape[0] * ratio)
        img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)

        test_image = face_recognition.load_image_file(location + example)

        # Find all the faces in the test image using the default HOG-based model
        face_locations = face_recognition.face_locations(test_image)
        no = len(face_locations)
        print("\n> There is/are '{1}' face(s) in image '{0}'".format(example, no))

        # Predict all the faces in the test image using the trained classifier

        if no > 0:
        
            for i in range(no):
                test_image_enc = face_recognition.face_encodings(test_image)[i]
                
                y = int(face_locations[i][0] * ratio) #top
                w = int(face_locations[i][1] * ratio) #right
                h = int(face_locations[i][2] * ratio) #bottom
                x = int(face_locations[i][3] * ratio) #left
                
                img = cv2.rectangle(img,(x,y),(w,h),(0,0,255),1)
                
                
                name = clf.predict([test_image_enc])
                name = ' '.join(str(*name).split('_'))
                
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(img, name, (x+4, h + 14), font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
                
                print("  -", name)
            

            cv2.imshow("Face Recognition", img)
            
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
        
face_recognize('./images/')
print('')