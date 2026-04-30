# Edge Detection Report

本次對 `ToBeDetect` 中兩張影像進行邊緣偵測：
- 一般影像：`windmill.webp`
- 醫學影像：`brain.webp`

使用方法（至少三種，實際四種）：
1. Sobel
2. Laplacian
3. Canny
4. LoG（Laplacian of Gaussian）

## 執行方式

```powershell
conda run -n MIP python edge_detection.py
```

或先啟用環境再執行：

```powershell
conda activate MIP
python edge_detection.py
```

輸出資料夾：`EdgeResults/`

## 前處理策略

- 一般影像（windmill）
  - 灰階化 + Gaussian Blur
  - 目的：降低高頻雜訊，同時保留主要輪廓。

- 醫學影像（brain）
  - 灰階化 + Median Blur + CLAHE + Gaussian Blur
  - 目的：醫學影像常有低對比與噪聲，CLAHE 可強化局部對比，Median 對雜點更穩定。

## 方法差異與優缺點

| 方法 | 核心概念 | 優點 | 缺點 | 在一般影像 | 在醫學影像 |
|---|---|---|---|---|---|
| Sobel | 一階梯度（x/y方向） | 計算快、方向資訊明確 | 對噪聲敏感，邊緣較厚 | 可清楚顯示風車葉片與建築輪廓 | 能顯示組織邊界趨勢，但細節易受噪聲干擾 |
| Laplacian | 二階導數（對強度變化敏感） | 可凸顯快速灰階變化 | 對噪聲更敏感，容易出現碎邊 | 紋理邊界很多，容易過度偵測 | 若未良好去噪，會放大醫學影像中的雜訊 |
| Canny | 平滑 + 梯度 + 非極大值抑制 + 雙閾值 | 邊緣細、連續性佳、抗噪性相對好 | 需調參（閾值） | 主體輪廓完整、背景雜邊較少 | 對組織輪廓的穩定度通常最好 |
| LoG | 先高斯平滑再做拉普拉斯 | 對小邊緣有偵測能力 | 參數不佳易過偵測 | 可抓到更多細節，但也可能帶來雜邊 | 對微小結構敏感，但可能把噪聲當邊界 |

## 結果檔案

- 一般影像整合圖：`EdgeResults/windmill/comparison_panel.png`
- 醫學影像整合圖：`EdgeResults/brain/comparison_panel.png`

每張影像另外輸出：
- `00_original_gray.png`
- `01_preprocessed.png`
- `02_sobel.png`
- `03_laplacian.png`
- `04_canny.png`
- `05_log.png`

## 結論

- 以本次設定來看，`Canny` 在兩類影像都較平衡，尤其在醫學影像上通常最穩定。
- `Sobel` 與 `Laplacian` 適合做梯度/細節分析輔助，不一定適合作為最終單一邊界。
- `LoG` 對細節敏感，適合需要捕捉微小結構時使用，但要搭配更嚴格去噪與閾值策略。
