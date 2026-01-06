# MoS2-Image-Synthesis-Platform

This tool facilitates STEM (Scanning Transmission Electron Microscopy) image simulation for Deep Learning and provides a general hub for working with atomic structures.


# 1. Generate Personalized XYZ and Params Files(100% Functional in current Version)

This module generates **custom atomic structure (XYZ)** files and corresponding **ComputeM parameter (params)** files for STEM image simulation of monolayer MoS₂, supporting both pristine and defective configurations.


### 📄 XYZ File (Atomic Structure)

The XYZ file contains the atomic coordinates and properties for the material structure.

**Example:**

```text
MoS2_incostem_10_17_1_Created_at_2024_12_26_15_30_45
31.5000 54.5660 1.0000
42 0.000000 0.000000 1.797500 1 0.08
16 1.575000 3.030889 0.000000 1 0.08
16 1.575000 3.030889 3.595000 1 0.08
42 1.575000 9.092667 1.797500 1 0.08
16 3.150000 12.123556 0.000000 1 0.08
16 3.150000 12.123556 3.595000 1 0.08
...
```

### ⚙️ Params File (STEM Simulation Parameters)

The params file contains the simulation parameters for ComputeM.

**Example:**

```text
MoS2_incostem_10_17_1_0.xyz
1 1 1
ImageMoS2_incostem_10_17_1_0.tif
512 512
300 -0.003 0.0 -50 21.4
70 200
END
0.45
30
y
12.5 1e-6
```

# 2. Generate STEM Images(100% Functional in current version)

<img width="300" height="295" alt="image" src="https://github.com/user-attachments/assets/e7da5daf-4f34-4e63-8e27-46b8c53ab148" />
<img width="300" height="500" alt="image" src="https://github.com/user-attachments/assets/575e1a05-6366-41fd-94c9-565da25f79fc" />

This step generates STEM `.tif` images by directly invoking **ComputeM** using the automatically generated XYZ and params files.

The resulting images are **equivalent** to those obtained when:
1. Manually creating the XYZ structure file  
2. Manually writing the corresponding params file  
3. Running both files independently through ComputeM  or in batches 
=

# Folder Workflow and Platform Facilitation (For 1 & 2)
- The platform safely interacts with the operating system to manage and organize output directories automatically, streamlining the large-scale, automated generation of STEM content.
  <img width="1313" height="677" alt="image" src="https://github.com/user-attachments/assets/1216e092-5d7d-4d3c-b18d-b3e49f731cba" />


# 3. Preprocessing(in progress)

This stage applies **physics-informed data augmentation and preprocessing** to the generated STEM images and their corresponding defect label maps. The goal is to bridge the gap between ideal simulated images and experimentally acquired STEM data, while preserving pixel-wise alignment between images and labels.

All transformations are applied **consistently across the image and all defect channels**.

---

**Applied Operations**
- **Image & label stacking**  
  Combines each STEM image with its associated defect masks into a unified array  
  `(N, X, Y, num_defects + 1)`

- **Horizontal shear**  
  Simulates horizontal sample drift during STEM acquisition using a Gaussian-distributed shear rate

- **Vertical constraint (scaling)**  
  Models vertical scan distortion caused by sample or beam instabilities

- **Rotation**  
  Aligns simulated images with experimental orientations or generates multi-orientation training data

- **Center cropping**  
  Removes blank regions introduced by affine transformations and enforces a fixed image size

- **Brightness & contrast adjustment**  
  Matches simulated image intensity statistics to real experimental images

- **Gaussian noise injection**  
  Adds detector and shot noise to approximate experimental signal variability

- **Random background addition**  
  Superimposes spatially varying, non-uniform backgrounds generated from a background image stack

---

**Output Formats**
- `.tiff` images for direct inspection and visualization  
- `.npy` arrays for efficient loading into deep learning pipelines  

The preprocessing step preserves **exact pixel-wise correspondence** between images and defect labels, making the output suitable for supervised learning tasks such as defect detection and segmentation in STEM images.

# 4. Deep Learning Models for Defect Detection(in progress, althought a model was created as an prototype)

This stage implements **two ResUNet-based convolutional neural networks** designed for pixel-wise analysis of STEM images of MoS₂.

The models are trained to detect and segment:
- **Vacancy defects** 
- **Polymorphs**

Each model operates on the preprocessed STEM images generated in the previous stages and produces spatially resolved probability maps aligned with the input images.

---

**Model Architecture**
- Backbone: **Residual U-Net (ResUNet)**
- Encoder–decoder structure with skip connections
- Residual blocks improve gradient flow and stability for deep architectures
- Designed for high-resolution, low-SNR STEM data

<img width="512" height="438" alt="image" src="https://github.com/user-attachments/assets/76db8361-7cd3-4222-9583-63006ef40069" />


---

**Outputs**
- Pixel-wise defect probability maps
- Separate output channels for different defect or polymorph classes
- Preserves exact spatial correspondence with the input STEM image

<img width="728" height="415" alt="image" src="https://github.com/user-attachments/assets/f83bf892-b013-4f8f-9779-b3eef3b1ceb1" />


The two-model setup allows specialization: one network focuses on **vacancy-type defects**, while the other targets **structural polymorph identification**, improving robustness and interpretability.

---



# Workflow 

## Overview(needs update)

The overall pipeline is implemented as a **modular, sequential workflow**, where each stage is handled by a dedicated Python module. Although not shown here, the internal execution follows a **graph-style flow** that mirrors the folder structure and data dependencies across the project.

At a high level, the workflow proceeds as follows:



<img width="1000" height="578" alt="image" src="https://github.com/user-attachments/assets/9cb96b07-5fe9-498b-8f1f-725d9f9fd5dc" />



### References

1. **ComputeM (STEM Simulation Software)**  
   ComputeM Development Team.  
   *ComputeM: Multislice STEM Simulation Toolbox.*  
   Page: https://sourceforge.net/projects/computem/ 
   
3. **Deep Learning of Vacancy Defects and Polymorphs in MoS₂**  
   Ziatdinov, M., Dyck, O., Maksov, A., Li, X., & Kalinin, S. V.  
   *Deep learning of atomically resolved scanning transmission electron microscopy images: identification of vacancy defects and polymorphs of MoS₂.*  
   **npj Computational Materials**, 3, 31 (2017).
   

5. **Deep Learning Enabled Measurements of Single-Atom Defects**  
   Lee, C.-H., Shi, C., Luo, D., Khan, A., Janicek, B. E., Kang, S., Zhu, W., Clark, B. K., & Huang, P. Y.  
   *Deep Learning Enabled Measurements of Single-Atom Defects in 2D Transition Metal Dichalcogenides with Sub-Picometer Precision.*  
   **Microscopy and Microanalysis**, 25(1), 172–181 (2019).  
   DOI: 10.1017/S1431927619001594
   <br>
   GitHub Repo:  https://github.com/Chuqiao2333/STEM-Simulation-Images/tree/master?tab=readme-ov-file





