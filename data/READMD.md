## Dataset

For each dataset, the test set JSON file includes the following fields:

- `image_path`: A list of image paths for studies with multiple images.
- `key_image_path`: The frontal image from the study for models that only support a single image as input.
- `context`: The context include  `age`: The age of the patient. `gender`: The gender of the patient. `indication`: The indication for the study. `comparison`: Comparison information if available.
- `frontal_lateral`: Corresponding view (frontal/lateral) for each image.
- `section_findings`: The findings of this study.
- `section_impression`: The impression of this study.
- `reports`: A concatenation of the findings and impression sections, in the format 'Findings: ' + `section_findings` + ' Impression: ' + `section_impression`.


## Dataset Details

### CheXpert Plus:   
*data_file*:  `./chexpert_plus/ReXRank_CheXpertPlus.json`  
*image_roor_dir*: `./chexpert_plus/PNG`


### MIMIC CXR:   
*datafile*:  `./mimic-cxr/ReXRank_MIMICCXR_test.json`  
*image_roor_dir*: `./mimic-cxr/files`


### IU X-ray:   
*datafile*:  `./iu_xray/ReXRank_IUXray_test.json`  
*image_roor_dir*: `./iu_xray/images`