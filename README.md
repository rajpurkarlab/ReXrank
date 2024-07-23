# ReXrank

ReXrank is an open-source leaderboard for AI-powered radiology report generation from chest x-ray images. We're setting a new standard in healthcare AI by providing a comprehensive, objective evaluation framework for cutting-edge models. Our mission is to accelerate progress in this critical field by fostering healthy competition and collaboration among researchers, clinicians, and AI enthusiasts.

![](./figures/new.gif) 
The detailed information of the test set has been updated in `./data/`. Check the details in `./data/README.md`.


## Overview

Using diverse datasets like MIMIC-CXR, IU-Xray, and CheXpert Plus, ReXrank offers a robust benchmarking system that evolves with clinical needs and technological advancements. Our leaderboard showcases top-performing models, driving innovation that could transform patient care and streamline medical workflows.

## Dataset

For each dataset, the test set JSON file includes the following fields:

- `image_path`: A list of image paths for studies with multiple images.
- `key_image_path`: The frontal image from the study for models that only support a single image as input.
- `context`: The context include  `age`: The age of the patient. `gender`: The gender of the patient. `indication`: The indication for the study. `comparison`: Comparison information if available.
- `frontal_lateral`: Corresponding view (frontal/lateral) for each image.
- `section_findings`: The findings of this study.
- `section_impression`: The impression of this study.
- `reports`: A concatenation of the findings and impression sections, in the format 'Findings: ' + `section_findings` + ' Impression: ' + `section_impression`.


### Dataset Details

-  CheXpert Plus:   
*data_file*:  `./chexpert_plus/ReXRank_CheXpertPlus.json`  
*image_roor_dir*: `./chexpert_plus/PNG`


-  MIMIC CXR:   
*datafile*:  `./mimic-cxr/ReXRank_MIMICCXR_test.json`  
*image_roor_dir*: `./mimic-cxr/files`

- IU X-ray:   
*datafile*:  `./iu_xray/ReXRank_IUXray_test.json`  
*image_roor_dir*: `./iu_xray/images`

## Join Us

Join us in shaping the future of AI-assisted radiology. Develop your models, submit your results, and see how you stack up against the best in the field. Together, we can push the boundaries of what's possible in medical imaging and report generation.

[Visit ReXrank](https://rajpurkarlab.github.io/ReXrank/)

## Contact
For any questions or suggestions, please open an issue or reach out to us at xiaomanzhang.zxm@gmail.com