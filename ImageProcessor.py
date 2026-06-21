import cv2
import numpy as np


def get_largest_contour(binary_img):
        """
        背景を除いた最大輪郭を取得する

        Parameters
        ----------
        binary_img : np.ndarray
            2値画像

        Returns
        -------
        contour : np.ndarray
            最大輪郭
        """
        contours, _ = cv2.findContours(binary_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        largest_contour = max(contours, key=cv2.contourArea)
        return largest_contour

def create_largest_region_mask(binary_img):
    """
    最大領域のみを残したマスクを生成
    """
    contour = get_largest_contour(binary_img)
    if contour is None:
        return np.zeros_like(binary_img)
    mask = np.zeros_like(binary_img)
    cv2.drawContours(mask,[contour],-1,255,thickness=cv2.FILLED)
    return mask

class ImageProcessor:

    @staticmethod
    def extract_largest_region(src_img, binary_img):
        """
        元画像から最大領域のみ抽出
        """

        binary_img = cv2.bitwise_not(binary_img)
        mask = create_largest_region_mask(binary_img)
        # cv2.imshow("Mask", mask)
        result = cv2.bitwise_and(
            src_img,
            src_img,
            mask=mask
        )

        return result
    
    @staticmethod
    def calculate_mean_value(image):
        """
        画像の平均値を計算する
        """
        if image is None:
            print("画像未選択平均値計算")
            return None
        mean_value = cv2.mean(image)[:3]  # BGRの平均値を取得
        return mean_value