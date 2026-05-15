import os
import random
import shutil

original_dataset_dir = "PetImages"

base_dir = "data1"

splits = ["train", "val", "test"]
classes = ["Cat", "Dog"]

for split in splits:
    for cls in classes:

        path = os.path.join(base_dir, split, cls)

        os.makedirs(path, exist_ok=True)

for cls in classes:

    source_dir = os.path.join(original_dataset_dir, cls)

    images = os.listdir(source_dir)

    random.shuffle(images)

    total = len(images)

    train_split = int(0.7 * total)
    val_split = int(0.15 * total)

    train_imgs = images[:train_split]
    val_imgs = images[train_split:train_split+val_split]
    test_imgs = images[train_split+val_split:]

    for img in train_imgs:

        src = os.path.join(source_dir, img)
        dst = os.path.join(base_dir, "train", cls, img)

        shutil.copyfile(src, dst)

    for img in val_imgs:

        src = os.path.join(source_dir, img)
        dst = os.path.join(base_dir, "val", cls, img)

        shutil.copyfile(src, dst)

    for img in test_imgs:

        src = os.path.join(source_dir, img)
        dst = os.path.join(base_dir, "test", cls, img)

        shutil.copyfile(src, dst)




















