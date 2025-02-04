import xml.etree.ElementTree as ET
import math


def calculate_center(box):
    """Calculate the center point of a bounding box."""
    return (
        (float(box['xtl']) + float(box['xbr'])) / 2,
        (float(box['ytl']) + float(box['ybr'])) / 2
    )


def calculate_distance(box1, box2):
    x1, y1 = calculate_center(box1)
    x2, y2 = calculate_center(box2)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def overlap(box1, box2):
    """Check if two boxes overlap."""
    return not (
            float(box1['xbr']) <= float(box2['xtl']) or
            float(box1['xtl']) >= float(box2['xbr']) or
            float(box1['ybr']) <= float(box2['ytl']) or
            float(box1['ytl']) >= float(box2['ybr'])
    )


def merge_boxes(boxes):
    """Merge overlapping boxes into a single bounding box."""
    xtl = min(float(box['xtl']) for box in boxes)
    ytl = min(float(box['ytl']) for box in boxes)
    xbr = max(float(box['xbr']) for box in boxes)
    ybr = max(float(box['ybr']) for box in boxes)

    return {
        'xtl': str(xtl),
        'ytl': str(ytl),
        'xbr': str(xbr),
        'ybr': str(ybr),
        'label': 'division'
    }


def process_annotations(input_file_path, output_file_path, distance_threshold):
    tree = ET.parse(input_file_path)
    root = tree.getroot()

    for image in root.findall('image'):
        boxes = [box for box in image.findall('box')]

        division_boxes = [box for box in boxes if box.attrib['label'] == 'division']
        cell_boxes = [box for box in boxes if box.attrib['label'] == 'cell']

        processed_boxes = set()

        # Process division boxes
        for i, box1 in enumerate(division_boxes):
            if box1 in processed_boxes:
                continue
            merge_candidates = [box1]
            for box2 in division_boxes:
                if box1 != box2 and box2 not in processed_boxes and overlap(box1.attrib, box2.attrib):
                    distance = calculate_distance(box1.attrib, box2.attrib)
                    if distance < distance_threshold:
                        merge_candidates.append(box2)

            if len(merge_candidates) > 1:
                merged_box = merge_boxes([box.attrib for box in merge_candidates])
                for box in merge_candidates:
                    image.remove(box)
                ET.SubElement(image, 'box', attrib=merged_box)
                processed_boxes.update(merge_candidates)

        # Update division labels only if they have overlapping division boxes
        for box1 in division_boxes:
            if any(overlap(box1.attrib, box2.attrib) for box2 in division_boxes if box1 != box2):
                box1.attrib['label'] = 'cell'

        # Process cell boxes
        processed_boxes = set()
        for i, box1 in enumerate(cell_boxes):
            if box1 in processed_boxes:
                continue
            merge_candidates = [box1]
            for box2 in cell_boxes:
                if box1 != box2 and box2 not in processed_boxes and overlap(box1.attrib, box2.attrib):
                    distance = calculate_distance(box1.attrib, box2.attrib)
                    if distance < distance_threshold:
                        merge_candidates.append(box2)

            if len(merge_candidates) > 1:
                merged_box = merge_boxes([box.attrib for box in merge_candidates])
                for box in merge_candidates:
                    image.remove(box)
                ET.SubElement(image, 'box', attrib=merged_box)
                processed_boxes.update(merge_candidates)

    # Save the modified XML
    tree.write(output_file_path, encoding='utf-8', xml_declaration=True)


# Example usage
process_annotations('annotations.xml', 'updated_annotations.xml', distance_threshold=13)
