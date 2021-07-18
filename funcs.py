from image import Image
import glob
import cv2


def allImagesInThisDirectory(directory):
    list_of_possible_formats = [
        "bmp",
        "pbm",
        "pgm",
        "ppm",
        "sr",
        "ras",
        "jpeg",
        "jpg",
        "jpe",
        "jp2",
        "tiff",
        "tif",
        "png",
    ]
    list_of_images_directory = list()
    for format in list_of_possible_formats:
        list_of_images_directory += glob.glob(directory + "\\*." + format)
    list_of_image_objects = [Image(x) for x in list_of_images_directory]
    return list_of_image_objects


# now let's initialize the list of reference point
ref_point = []
crop = False


def eazyCrop(image):
    def shape_selection(event, x, y, flags, param):
        # grab references to the global variables
        global ref_point, crop

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being performed
        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            ref_point.append((x, y))

            # draw a rectangle around the region of interest
            cv2.rectangle(image, ref_point[0], ref_point[1], (255, 0, 255), 2)
            cv2.imshow("image", image)

    # load the image, clone it, and setup the mouse callback function
    clone = image.copy()
    image = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # if the 'c' key is pressed, break from the loop
        elif key == ord("c"):
            break

    if len(ref_point) == 2:
        crop_img = clone[
            min(ref_point[0][1], ref_point[1][1]) : max(
                ref_point[0][1], ref_point[1][1]
            ),
            min(ref_point[0][0], ref_point[1][0]) : max(
                ref_point[0][0], ref_point[1][0]
            ),
        ]
        return crop_img


def label(image, save=False):
    def shape_selection(event, x, y, flags, param):
        # grab references to the global variables
        global ref_point, crop

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being performed
        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            ref_point.append((x, y))

            # draw a rectangle around the region of interest
            cv2.rectangle(image, ref_point[0], ref_point[1], (255, 0, 255), 2)
            cv2.imshow("image", image)

    # load the image, clone it, and setup the mouse callback function
    clone = image.copy()
    if save == False:
        image = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", shape_selection)

    # keep looping until the 'q' key is pressed
    while True:
        # display the image and wait for a keypress
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # if the 'l' key is pressed, break from the loop
        elif key == ord("l"):
            break

    if len(ref_point) == 2:
        x = (ref_point[0][0] + ref_point[1][0]) // 2
        y = (ref_point[0][1] + ref_point[1][1]) // 2
        print("Please enter the text:")
        text = input()
        cv2.putText(
            image,
            text,
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 255),
            2,
        )
        return [image, ref_point, x, y, text]
