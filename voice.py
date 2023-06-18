from keras.models import load_model
import numpy as np
import librosa

audio_model = load_model('audio_classification.hdf5')

def features_extractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast')
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T,axis=0)
    return mfccs_scaled_features

def audio_predict(filename):
    # filename="audio_test/olsfly.wav"
    prediction_feature=features_extractor(filename)
    prediction_feature=prediction_feature.reshape(1,-1)
    predicted_probabilities = audio_model.predict(prediction_feature)
    predicted_class = np.argmax(predicted_probabilities)
    print(predicted_probabilities)
    print(predicted_class)

    # Example assuming you have a list of class labels
    # class_labels = ["Olive-sided Flycatcher", "Orange-crowned Warbler", "Western Osprey","Ovenbird"]
    class_labels = ["olsfly", "orcwar", "osprey","ovenbi1"]

    predicted_label = class_labels[predicted_class]

    # print("Predicted class label:", predicted_label)
    return "Predicted class label:", predicted_label