import cv2
import os
import glob


def filter_and_classify_images():
    # Get list of filenames starting with 'WIN'
    win_files = (
        glob.glob("Bed Photo/WIN*.jpg")
        + glob.glob("Bed Photo/WIN*.jpeg")
        + glob.glob("Bed Photo/WIN*.png")
    )

    if not win_files:
        print("No files found starting with 'WIN'")
        return

    print(f"Found {len(win_files)} files starting with 'WIN'")

    # Counter for numbering
    count = 1

    for filename in win_files:
        # Read the image
        img = cv2.imread(filename)

        if img is None:
            print(f"Could not open image: {filename}")
            continue

        # Display image
        cv2.imshow("Image Classification", img)
        print(f"Image: {filename}")
        print("Press '1' for crumpled, '2' for uncrumpled, 'q' to quit")

        # Wait for key press
        while True:
            key = cv2.waitKey(0) & 0xFF

            if key == ord("1"):  # Crumpled
                crumple_status = "crumpled2"
                break
            elif key == ord("2"):  # Uncrumpled
                crumple_status = "uncrumpled2"
                break
            elif key == ord("q"):  # Quit
                cv2.destroyAllWindows()
                print("Classification cancelled by user")
                return
            else:
                print(
                    "Invalid key! Press '1' for crumpled, '2' for uncrumpled, 'q' to quit"
                )

        # Create new filename
        name, ext = os.path.splitext(filename)
        new_filename = f"top_{count}_{crumple_status}{ext}"

        # Rename the file
        try:
            os.rename(filename, new_filename)
            print(f"Renamed: {filename} -> {new_filename}")
            count += 1
        except OSError as e:
            print(f"Error renaming file {filename}: {e}")

    cv2.destroyAllWindows()
    print("Classification completed!")


if __name__ == "__main__":
    filter_and_classify_images()
