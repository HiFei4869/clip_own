import os
from PIL import Image

def load_and_preprocess_images_from_folder(folder_path):
    image_extensions = ('.jpg', '.jpeg')  # Supported image formats
    images = []
    image_names = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(image_extensions):
            image_path = os.path.join(folder_path, filename)
            try:
                image = Image.open(image_path).convert('RGB')
                images.append(image)
                image_names.append(filename)  # Append filename to image_names list
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")

    return images, image_names

def generate_subset(images_all, indices):
    images = []
    for i in indices:
        images.append(images_all[i])
    return images

def merge_images(images):
    # Calculate mean width and height
    mean_width = sum(img.width for img in images) // len(images)
    mean_height = sum(img.height for img in images) // len(images)

    # Scale images to not exceed mean width and height
    scaled_images = []
    for img in images:
        if img.width > mean_width or img.height > mean_height:
            # Determine scaling factor to keep the aspect ratio
            width_scale = mean_width / img.width
            height_scale = mean_height / img.height
            scale = min(width_scale, height_scale)
            new_width = int(img.width * scale)
            new_height = int(img.height * scale)
            scaled_img = img.resize((new_width, new_height), Image.LANCZOS)
        else:
            scaled_img = img
        scaled_images.append(scaled_img)
    
    # Determine the number of columns and rows
    num_images = len(images)
    num_cols = int(num_images ** 0.5) or 1
    num_rows = (num_images + num_cols - 1) // num_cols

    # Calculate the dimensions of the big image based on the grid size
    big_width = mean_width * num_cols
    big_height = mean_height * num_rows

    # Create a blank big image with white background
    big_image = Image.new('RGB', (big_width, big_height), color='white')

    # Paste each image onto the big image within the grid
    offset_x = 0
    offset_y = 0
    for idx, scaled_img in enumerate(scaled_images):
        big_image.paste(scaled_img, (offset_x, offset_y))
        offset_x += mean_width
        if offset_x >= big_width:
            offset_x = 0
            offset_y += mean_height

    return big_image

# Example usage:
folder_path = "./drawings_big"
images, image_names = load_and_preprocess_images_from_folder(folder_path)
#merged_image = merge_images(images)

# clustering:
indices_0 = [1, 8, 10, 11, 12, 16, 28, 41, 45, 46, 56, 75, 77, 79, 81, 97, 98, 101, 105, 109, 113, 118, 121, 123, 124, 125, 126, 127, 128, 132, 133, 135, 136, 137, 138, 139, 140, 141, 142, 144, 145, 149, 151, 154, 155, 157, 158, 159, 160, 163, 165, 166, 167, 170, 171, 172, 174, 176, 177, 180, 182, 186, 188, 189, 190, 191, 193, 194, 196, 198, 199, 209, 211, 220, 222, 224, 225, 226, 231, 233, 236, 237, 239, 240, 241, 242, 244, 254, 255, 256, 259, 264, 265, 269, 275, 278, 280, 285, 286, 291, 293, 298, 301, 303, 308, 309, 311, 313, 315, 319, 322, 324, 327, 328, 329, 330, 335, 336, 337, 338, 339, 341, 344, 345, 355, 358, 359, 364, 365, 374, 375, 380, 382, 389, 390, 391, 392, 395, 396, 397, 399, 405, 406, 410, 414, 416, 418, 419, 420, 421, 422, 425, 427, 428, 429, 430, 431, 434, 435, 436, 438, 441, 443, 446, 455, 456, 463, 465, 466, 469, 473, 474, 477, 479, 480, 482, 483, 491, 492, 494, 495, 498, 502, 503, 512, 514, 518, 519, 521, 525, 528, 531, 532, 539, 540, 542, 544, 548, 549, 550, 557, 558, 559, 561, 563, 564, 567, 568, 576, 582, 584, 585, 586, 590, 601, 603, 606, 608, 611, 616, 618, 625, 633, 635, 636, 637, 640, 651, 655, 657, 658, 663, 666, 671, 673, 676, 692, 693, 695, 698, 699, 700, 702, 704, 707, 710, 712, 713, 715, 717, 720, 723, 727, 728, 731, 735, 743, 744, 753, 762, 764, 765, 770, 771, 779, 785, 787, 792, 796, 805, 809, 811, 812, 816, 818, 820, 829, 831, 833, 839, 841, 842, 846, 850, 853, 854, 856, 860, 865, 868, 870, 872, 873, 875, 876, 878, 882, 883, 884, 886, 887, 889, 899, 900, 901, 904, 907, 910, 913, 921, 927, 932, 935, 941, 954, 958, 961, 964, 970, 977, 978, 982, 986, 987, 999, 1002, 1006, 1010, 1012, 1018, 1021, 1029, 1033, 1035, 1038, 1042, 1043, 1044, 1045, 1050, 1052, 1056, 1058, 1061, 1066, 1072, 1073, 1075, 1088]

indices_1 = [5, 6, 7, 9, 14, 17, 20, 21, 30, 31, 32, 33, 37, 38, 40, 42, 43, 47, 48, 49, 50, 51, 52, 53, 54, 55, 58, 68, 70, 71, 73, 74, 76, 88, 89, 91, 112, 122, 152, 153, 173, 215, 221, 235, 249, 250, 258, 268, 272, 273, 282, 284, 294, 302, 312, 321, 334, 340, 347, 350, 354, 361, 381, 385, 460, 468, 471, 475, 487, 488, 489, 497, 501, 508, 534, 555, 565, 566, 570, 571, 577, 579, 583, 587, 588, 589, 593, 597, 598, 605, 614, 620, 646, 653, 674, 679, 686, 687, 688, 694, 696, 722, 729, 736, 738, 745, 746, 747, 750, 751, 775, 789, 790, 799, 803, 822, 827, 838, 844, 849, 862, 864, 877, 885, 891, 916, 928, 962, 965, 976, 985, 992, 995, 1005, 1015, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1030, 1031, 1034, 1041, 1046, 1047, 1048, 1049, 1053, 1054, 1055, 1057, 1062, 1063, 1064, 1067, 1070, 1071, 1074, 1076, 1078, 1080, 1093, 1105, 1106]

indices_2 = [0, 4, 13, 18, 19, 24, 25, 44, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67, 69, 78, 84, 168, 178, 179, 183, 184, 185, 187, 203, 227, 245, 247, 251, 253, 270, 274, 290, 306, 320, 370, 388, 403, 409, 424, 459, 467, 490, 493, 507, 527, 530, 536, 541, 573, 591, 609, 613, 619, 628, 647, 659, 681, 684, 690, 739, 742, 749, 756, 794, 806, 814, 826, 837, 845, 851, 852, 871, 881, 898, 914, 924, 947, 951, 984, 1003, 1032, 1037, 1039, 1059, 1068, 1069, 1077, 1079, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1089, 1090, 1091, 1092, 1094, 1096, 1097, 1099, 1100, 1101, 1102, 1103, 1104]

indices_3 = [2, 3, 15, 22, 23, 26, 27, 29, 34, 35, 36, 39, 92, 115, 129, 130, 131, 134, 143, 146, 150, 156, 161, 162, 164, 169, 175, 192, 195, 201, 204, 205, 207, 208, 210, 212, 230, 252, 257, 260, 263, 266, 267, 277, 281, 287, 289, 292, 299, 304, 305, 307, 310, 318, 326, 331, 332, 343, 351, 352, 353, 362, 366, 367, 368, 372, 373, 376, 377, 383, 384, 386, 387, 394, 401, 402, 408, 413, 439, 442, 444, 448, 450, 453, 454, 457, 464, 470, 484, 499, 504, 511, 513, 517, 520, 523, 524, 526, 537, 538, 551, 556, 562, 575, 595, 596, 599, 610, 612, 622, 623, 629, 631, 639, 644, 661, 662, 664, 668, 675, 683, 689, 691, 701, 711, 741, 748, 755, 772, 773, 791, 800, 802, 823, 828, 835, 859, 874, 879, 892, 893, 894, 902, 906, 912, 922, 934, 936, 937, 942, 945, 953, 960, 966, 971, 972, 975, 990, 997, 1009, 1016, 1095, 1098]

indices_4 = [72, 80, 82, 83, 85, 86, 87, 90, 93, 94, 95, 96, 99, 100, 102, 103, 104, 106, 107, 108, 110, 111, 114, 116, 117, 119, 120, 147, 148, 181, 197, 200, 202, 206, 213, 214, 216, 217, 218, 219, 223, 228, 229, 232, 234, 238, 243, 246, 248, 261, 262, 271, 276, 279, 283, 288, 295, 296, 297, 300, 314, 316, 317, 323, 325, 333, 342, 346, 348, 349, 356, 357, 360, 363, 369, 371, 378, 379, 393, 398, 400, 404, 407, 411, 412, 415, 417, 423, 426, 432, 433, 437, 440, 445, 447, 449, 451, 452, 458, 461, 462, 472, 476, 478, 481, 485, 486, 496, 500, 505, 506, 509, 510, 515, 516, 522, 529, 533, 535, 543, 545, 546, 547, 552, 553, 554, 560, 569, 572, 574, 578, 580, 581, 592, 594, 600, 602, 604, 607, 615, 617, 621, 624, 626, 627, 630, 632, 634, 638, 641, 642, 643, 645, 648, 649, 650, 652, 654, 656, 660, 665, 667, 669, 670, 672, 677, 678, 680, 682, 685, 697, 703, 705, 706, 708, 709, 714, 716, 718, 719, 721, 724, 725, 726, 730, 732, 733, 734, 737, 740, 752, 754, 757, 758, 759, 760, 761, 763, 766, 767, 768, 769, 774, 776, 777, 778, 780, 781, 782, 783, 784, 786, 788, 793, 795, 797, 798, 801, 804, 807, 808, 810, 813, 815, 817, 819, 821, 824, 825, 830, 832, 834, 836, 840, 843, 847, 848, 855, 857, 858, 861, 863, 866, 867, 869, 880, 888, 890, 895, 896, 897, 903, 905, 908, 909, 911, 915, 917, 918, 919, 920, 923, 925, 926, 929, 930, 931, 933, 938, 939, 940, 943, 944, 946, 948, 949, 950, 952, 955, 956, 957, 959, 963, 967, 968, 969, 973, 974, 979, 980, 981, 983, 988, 989, 991, 993, 994, 996, 998, 1000, 1001, 1004, 1007, 1008, 1011, 1013, 1014, 1017, 1019, 1020, 1036, 1040, 1051, 1060, 1065]

images_cluster_0 = generate_subset(images, indices_0)
images_cluster_1 = generate_subset(images, indices_1)
images_cluster_2 = generate_subset(images, indices_2)
images_cluster_3 = generate_subset(images, indices_3)
images_cluster_4 = generate_subset(images, indices_4)

images_0 = merge_images(images_cluster_0)
images_1 = merge_images(images_cluster_1)
images_2 = merge_images(images_cluster_2)
images_3 = merge_images(images_cluster_3)
images_4 = merge_images(images_cluster_4)
# Save the merged image to a file
#merged_image.save("data_show_big.jpg")  # Change the file extension as needed
images_0.save("data_show_cluster_0.png")
images_1.save("data_show_cluster_1.png")
images_2.save("data_show_cluster_2.png")
images_3.save("data_show_cluster_3.png")
images_4.save("data_show_cluster_4.png")
