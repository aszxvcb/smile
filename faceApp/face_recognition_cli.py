# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
import re
import face_recognition.api as face_recognition
import multiprocessing
import itertools
import sys
import PIL.Image
import numpy as np

import json
from collections import OrderedDict

def upload_unknown_file(upload_file): #업로드된 파일들 검사 후 배열에 저장

    upload_name = upload_file;

    print("[check] upload_unknown_file : {}".format(upload_file));

    upload_image = face_recognition.load_image_file(upload_file)

    if(max(upload_image.shape) > 1600):
        pil_img = PIL.Image.fromarray(upload_image)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS) # 크기 줄임
        upload_image = np.array(pil_img)

    upload_encodings = face_recognition.face_encodings(upload_image)
    #TODO. upload_encodings 실패시 예외처리 추가 , jpeg의 경우 인코딩이 안되는 경우 종종 발생. 확인 필요

    print("[check] upload_encodings " , upload_encodings);

    if (not os.path.isfile("./media/unknown/unknown_encodings_save.json")):
        upload_data = {};
        upload_data["unknowns"] = [];
    else:
        with open("./media/unknown/unknown_encodings_save.json", "r") as f:
            upload_data = json.load(f);

    # numpy 를 array 로 변환
    upload_encodings = np.array(upload_encodings)

    upload_data["unknowns"].append({"name":upload_name.name, "encodings":upload_encodings.tolist()})
    # python 'with'는 파일을 다룰 때 사용
    # 파일을 오픈하고 json_file 로 alias, .dump() 은 json을 해당 파일포인터로 파싱
    with open("./media/unknown/unknown_encodings_save.json", "w", encoding="utf=8") as json_file:
        json.dump(upload_data, json_file, ensure_ascii=False, indent="\t")

    print("encoding file save complete!")


def selfie_upload_btn(selfie_file, user_id): # 유저의 셀피를 올려 자신이 나온 사진을 다운로드 받는 함수

    print("[check] selfie_upload_bth : {}".format(selfie_file));

    # 유저의 셀피를 분석
    img = face_recognition.load_image_file(selfie_file)

    #Check. 인코딩이 왜 오래걸리지?
    user_encodings = face_recognition.face_encodings(img)

    if len(user_encodings) > 1:
        click.echo("WARNING: More than one face found in {}. Only considering the first face.".format(selfie_file))
        #TODO. 얼굴이 두개 이상 발견 시 에러 프론트로 전달
    if len(user_encodings) == 0:
        click.echo("WARNING: No faces found in {}. Ignoring file.".format(selfie_file))
        #TODO. 얼굴 발견되지 않을 시 에러 프론트로 전달

    # TODO. 사진들 속에서 유저의 얼굴이 나온 사진을 검출
    file_path="./media/known/" + user_id.username + "/known_encodings_save.json"

    # selfie 인코딩 파일은 사진 하나에 대해서만 존재해야함. 기존 인코딩이 존재하면 삭제
    if (os.path.isfile(file_path)):
        os.remove(file_path)

    upload_data = {};
    upload_data["unknowns"] = [];

    # numpy 를 array 로 변환
    upload_encodings = np.array(user_encodings)

    upload_data["unknowns"].append({"name":user_id.username, "encodings":upload_encodings.tolist()})
    # python 'with'는 파일을 다룰 때 사용
    # 파일을 오픈하고 json_file 로 alias, .dump() 은 json을 해당 파일포인터로 파싱
    with open(file_path, "w", encoding="utf=8") as json_file:
        json.dump(upload_data, json_file, ensure_ascii=False, indent="\t")

def compare_image(image_to_check, known_names, known_face_encodings, tolerance=0.3, show_distance=False):
    # 유저의 얼굴이 포함된 사진 이름 리스트
    user_faces = []

    with open("./media/unknown/unknown_encodings_save.json", "r") as json_file:
        json_data = json.load(json_file)

    for unknown in json_data['unknowns']:
        unknown_encodings = np.array(unknown['encodings'])
        number_of_people = unknown_encodings.ndim # 한 명인지 한 명 이상인지만 판단

        if(number_of_people==1): # 사진 속 사람이 한 명일 경우
            distances = face_recognition.face_distance(known_face_encodings, unknown_encodings)
            result = list(distances <= tolerance)

            if True in result:
                user_faces.append(unknown['name'])

        else: # 사진 속에 2명 이상의 사람이 있을 경우
            number_of_people = unknown_encodings.shape[0] # 몇 명인지 정확하게
            # 유저가 사진에 몇명이 나왔는 지 여부 확인


            for unknown_encoding in unknown_encodings:
                distances = face_recognition.face_distance(known_face_encodings, unknown_encoding)
                result = list(distances <= tolerance)
                print(unknown['name'], " : ", distances);
                if True in result:
                    user_faces.append(unknown['name'])
                    continue
    print(user_faces);
    return user_faces


def image_files_in_folder(folder): # pwd 효과
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]


def process_images_in_process_pool(images_to_check, known_names, known_face_encodings, number_of_cpus, tolerance, show_distance):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    # macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(known_names),
        itertools.repeat(known_face_encodings),
        itertools.repeat(tolerance),
        itertools.repeat(show_distance)
    )

    pool.starmap(test_image, function_parameters)


@click.command()
@click.argument('known_people_folder')
@click.argument('image_to_check')
@click.option('--cpus', default=1, help='number of CPU cores to use in parallel (can speed up processing lots of images). -1 means "use all in system"')
@click.option('--tolerance', default=0.6, help='Tolerance for face comparisons. Default is 0.6. Lower this if you get multiple matches for the same person.')
@click.option('--show-distance', default=False, type=bool, help='Output face distance. Useful for tweaking tolerance setting.')
def main(known_people_folder, image_to_check, cpus, tolerance, show_distance):
    # known_names, known_face_encodings = scan_known_people(known_people_folder)

    # Multi-core processing only supported on Python 3.4 or greater
    if (sys.version_info < (3, 4)) and cpus != 1:
        click.echo("WARNING: Multi-processing support requires Python 3.4 or greater. Falling back to single-threaded processing!")
        cpus = 1
"""
    if os.path.isdir(image_to_check):
        if cpus == 1:
            [test_image(image_file, known_names, known_face_encodings, tolerance, show_distance) for image_file in image_files_in_folder(image_to_check)]
        else:
            process_images_in_process_pool(image_files_in_folder(image_to_check), known_names, known_face_encodings, cpus, tolerance, show_distance)
    else:
        test_image(image_to_check, known_names, known_face_encodings, tolerance, show_distance)

"""
if __name__ == "__main__":
    main()
