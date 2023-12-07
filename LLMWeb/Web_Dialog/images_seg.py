import os
from tqdm import tqdm
from PIL import Image
import numpy as np
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from models.unet import U2NET
from utils import Normalize_image, load_checkpoint_mgpu

import cv2


device = "cuda" if torch.cuda.is_available() else "cpu"
checkpoint_path = './models/trained_checkpoint/cloth_segm.pth'
output_dir = './output_image/'


# Note that the height is in the cm unit
def image_segment(image_dir, height):

    def get_palette(num_cls):
        """ Returns the color map for visualizing the segmentation mask.
        Args:
            num_cls: Number of classes
        Returns:
            The color map
        """
        n = num_cls
        palette = [0] * (n * 3)
        for j in range(0, n):
            lab = j
            palette[j * 3 + 0] = 0
            palette[j * 3 + 1] = 0
            palette[j * 3 + 2] = 0
            i = 0
            while lab:
                palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
                palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
                palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
                i += 1
                lab >>= 3
        return palette
    

    transforms_list = []
    transforms_list += [transforms.ToTensor()]
    transforms_list += [Normalize_image(0.5, 0.5)]
    transform_rgb = transforms.Compose(transforms_list)

    net = U2NET(in_ch=3, out_ch=4).to(device)
    # print(net)

    print(os.path.exists(checkpoint_path))
    net = load_checkpoint_mgpu(net, checkpoint_path)
    net.eval()

    palette = get_palette(4)

    # images_list = sorted(os.listdir(image_dir))
    # pbar = tqdm(total = len(images_list))

    # for image_name in images_list:
    img = Image.open(image_dir).convert('RGB')
    img_size = img.size
    img = img.resize((768, 768))
    image_tensor = transform_rgb(img)
    image_tensor = torch.unsqueeze(image_tensor, 0)
    image_name = os.path.basename(image_dir)

    output_tensor = net(image_tensor.to(device))
    output_tensor = F.log_softmax(output_tensor[0], dim=1)
    output_tensor = torch.max(output_tensor, dim=1, keepdim=True)[1]
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_tensor = torch.squeeze(output_tensor, dim=0)
    output_arr = output_tensor.cpu().numpy()

    output_img = Image.fromarray(output_arr.astype('uint8'), mode='L')
    output_img = output_img.resize(img_size, Image.BICUBIC)
    
    segmented_image_path = os.path.join(output_dir, image_name[:-4]+'_generated.png')

    output_img.putpalette(palette)
    output_img.save(segmented_image_path)

    plt.imshow(output_img)
    plt.title(image_name)

    # Get Mask

    img = cv2.imread(image_dir)
    output_img = Image.open(segmented_image_path)
    output_arr = np.array(output_img)
    binary_mask = (output_arr > 0).astype(np.uint8) * 255

    # bounding box
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow('Image 1',img)

    # # segment
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 5)

    cv2.imshow('Image 2', img)


    def calculate_real_world_dimensions(contour, pixels_per_metric):
        x, y, w, h = cv2.boundingRect(contour)
        width = w / pixels_per_metric
        height = h / pixels_per_metric
        return width, height
    
    def draw_double_arrowed_line(image, start, end, color, thickness, tipLength):
        cv2.arrowedLine(image, start, end, color, thickness, tipLength=tipLength)
        cv2.arrowedLine(image, end, start, color, thickness, tipLength=tipLength)


    def display_dimensions_on_image(img, binary_mask, real_object_height, offset = 0):
        contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = max(contours, key=cv2.contourArea)
        _, _, _, h = cv2.boundingRect(largest_contour)
        pixels_per_metric = h / real_object_height

        for contour in contours:
            width, height = calculate_real_world_dimensions(contour, pixels_per_metric)
            x, y, w, h = cv2.boundingRect(contour)
           
            arrow_start_length = (x + w + offset, y + h)
            arrow_end_length = (x + w + offset, y)
            draw_double_arrowed_line(img, arrow_start_length, arrow_end_length, (255, 0, 0), 2, 0.01)
            cv2.putText(img, f"{height:.2f}", ((x + w + offset + 10), y + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

            arrow_start_height = (x, y + h + offset)
            arrow_end_height = (x + w, y + h + offset)
            draw_double_arrowed_line(img, arrow_start_height, arrow_end_height, (255, 0, 0), 2, 0.01)
            cv2.putText(img, f"{width:.2f}", (x + w//2, y + h + offset + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        
        return img

    real_object_height = height
    img_with_dimensions = display_dimensions_on_image(img, binary_mask, real_object_height)

    cv2.imshow('Image 3', img_with_dimensions)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_dir = "./input_image/bag1.png"
    height = 170
    image_segment(image_dir, height)