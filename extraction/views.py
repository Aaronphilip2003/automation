from django.shortcuts import render
from django.http import HttpResponse
import geopandas as gpd
import pandas as pd


def say_hello(request):
    return HttpResponse("Hello World")

def proc(request):
    return render(request,'hello.html')

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def extract_points_within_polygon(dataset_path: str, point_path: str):
    # Load the input datasets
    dataset = gpd.read_file(dataset_path)
    point = gpd.read_file(point_path)
    
    # Loop over each admin ward polygon and extract points within it
    extracted_points = []
    for _, ward in dataset.iterrows():
        points_within_ward = point[point.within(ward.geometry)]
        extracted_points.append(points_within_ward)
    
    # Concatenate all extracted points and export to CSV
    extracted_points = pd.concat(extracted_points)
    extracted_points.to_csv("Extracted-Aaron2.csv", index=False)


def upload_files(request):
    if request.method == 'POST' and 'dataset' in request.FILES and 'point' in request.FILES:
        # Retrieve the uploaded files from the request
        dataset_file = request.FILES['dataset']
        point_file = request.FILES['point']

        # Save the uploaded files temporarily
        fs = FileSystemStorage()
        dataset_path = fs.save(dataset_file.name, dataset_file)
        point_path = fs.save(point_file.name, point_file)

        # Run the extraction function
        extract_points_within_polygon(dataset_path, point_path)

        # Provide a download link for the generated file
        extracted_file_name = "Extracted-Aaron2.csv"
        extracted_file_url = fs.url(extracted_file_name)

        return render(request, 'result.html', {'extracted_file_url': extracted_file_url})

    return render(request, 'upload.html')