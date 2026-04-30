# G1-MIP-BonusQuestion

使用至少三種邊緣偵測方法，對 `ToBeDetect/` 中兩張影像進行偵測：
- 一般影像：`windmill.webp`
- 醫學影像：`brain.webp`

本專案實作方法：
- Sobel
- Laplacian
- Canny
- LoG (Laplacian of Gaussian)

## 專案結構

```text
.
├─ ToBeDetect/
│  ├─ windmill.webp
│  └─ brain.webp
├─ edge_detection.py
├─ EdgeResults/
│  ├─ windmill/
│  └─ brain/
└─ EDGE_METHODS_REPORT.md
```

## 環境需求

- Python 3.11
- `opencv-python-headless`
- `numpy`
- `pillow`

目前已使用 **名稱型 conda 環境**：`MIP`

## 執行方式

方法 1：不啟用環境，直接執行

```powershell
conda run -n MIP python edge_detection.py
```

方法 2：先啟用環境再執行

```powershell
conda activate MIP
python edge_detection.py
```

## 輸出結果

執行後會產生：
- `EdgeResults/windmill/`
- `EdgeResults/brain/`

每張影像輸出：
- `00_original_gray.png`
- `01_preprocessed.png`
- `02_sobel.png`
- `03_laplacian.png`
- `04_canny.png`
- `05_log.png`
- `comparison_panel.png`（整合比較圖）

## 方法比較報告

詳細的方法差異與優缺點整理在：
- `EDGE_METHODS_REPORT.md`
