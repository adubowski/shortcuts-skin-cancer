# Shortcut Learning in Machine Learning Models for Skin Cancer Diagnosis
The project aims to show the undesired bias in skin cancer prediction models when trained on the ISIC dataset which contains coloured patches in the group of non-cancer images, which could potentially result in misdiagnoses when applied in real-life scenarios.

Corresponding Paper: ["Uncovering and Correcting Shortcut Learning in Machine Learning Models for Skin Cancer Diagnosis"](https://www.mdpi.com/2075-4418/12/1/40)

### Abstract
Machine learning models have been successfully applied for analysis of skin images. However, due to the black box nature of such deep learning models, it is difficult to understand their underlying reasoning. This prevents a human from validating whether the model is right for the right reasons. Spurious correlations and other biases in data can cause a model to base its predictions on such artefacts rather than on the true relevant information. These learned shortcuts can in turn cause incorrect performance estimates and can result in unexpected outcomes when the model is applied in clinical practice. 

This study presents a method to detect and quantify this shortcut learning in trained classifiers for skin cancer diagnosis, since it is known that dermoscopy images can contain artefacts. Specifically, we train a standard VGG16-based skin cancer classifier on the public ISIC dataset, for which colour calibration charts (elliptical, coloured patches) occur only in benign images and not in malignant ones. Our methodology artificially inserts those patches and uses inpainting to automatically remove patches from images to assess the changes in predictions. We find that our standard classifier partly bases its predictions of benign images on the presence of such a coloured patch. More importantly, by artificially inserting coloured patches into malignant images, we show that shortcut learning results in a significant increase in misdiagnoses, making the classifier unreliable when used in clinical practice. With our results, we, therefore, want to increase awareness of the risks of using black box machine learning models trained on potentially biased datasets. Finally, we present a model-agnostic method to neutralise shortcut learning by removing the bias in the training dataset by exchanging coloured patches with benign skin tissue using image inpainting and re-training the classifier on this de-biased dataset

### Code
Makes use of code from https://github.com/laura-rieger/deep-explanation-penalization for handling the ISIC Skin Cancer dataset & training a VGG16 classifier to distinguish between malignant and benign lesions. The segmentation masks for identifying the coloured patches in the image are also taken from here.

Uses the GMCNN inpainting model from: https://github.com/shepnerd/inpainting_gmcnn/tree/master/pytorch

More specific detail on which code is copied or original is available either in the sub-directories or at the top of the individual notebooks themselves.

Overall workflow:

1. Download & resize images from ISIC database                      *(01_process_data - scripts 00 to 02).*
2. Dilate the patch segmentation masks                              *(01_process_data - 03_dilate_masks.py).*
3. Train the inpainting model                                       *(02_inpainting - inpainting_gmcnn_train.ipynb).*
4. Apply inpainting to the relevant images for experiments          *(02_inpainting - inpainting_gmcnn_test.ipynb).*
5. Train the classifier on the original images or inpainted images  *(03_classifier - train_classifier.ipynb).*
6. Run experiments as reported in the paper                         *(03_classifier - compare_predictions.ipynb).*

### Citations
Corresponding Paper (peer-reviewed, open access): ["Uncovering and Correcting Shortcut Learning in Machine Learning Models for Skin Cancer Diagnosis"](https://www.mdpi.com/2075-4418/12/1/40). Please cite this paper when using the code: 
```
@article{nauta2022uncovering,
  title={Uncovering and Correcting Shortcut Learning in Machine Learning Models for Skin Cancer Diagnosis},
  author={Nauta, Meike and Walsh, Ricky and Dubowski, Adam and Seifert, Christin},
  journal={Diagnostics},
  volume={12},
  number={1},
  pages={40},
  year={2022},
  publisher={Multidisciplinary Digital Publishing Institute}
}
```
