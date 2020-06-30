import os
import zipfile
import random
from io import StringIO
import threading
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import *
from .templates import *
from .course_wrapper import *
from .cytoscape import *
from django import forms
from shutil import make_archive
from wsgiref.util import FileWrapper
import time


files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '', "unique_id": '',
                    "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0,
                    "msa_phylo": True, "outdir": ''}

metadata_dictionary = {"metadata": ''}


def call_course_wrapper(type, dict, metadata_dict):
    eval(type)(dict, metadata_dict)


def main_page(request):
    html = 'main_page.html'
    context = {}
    template = loader.get_template(html)
    return HttpResponse(template.render(context, request))


def anacapa(request):
    context = {}
    context['form'] = AnacapaForm()
    if request.method == 'POST':
        form = AnacapaForm(request.POST, request.FILES)
        if form.is_valid():
            anacapa_dict = files_dictionary
            anacapa_metadata_dict = metadata_dictionary
            anacapa_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
            anacapa_dict['otutable'] = form.cleaned_data['otu_table'].file.name
            anacapa_dict['fwdseq'] = form.cleaned_data['forward_seqs'].file.name
            anacapa_dict['mergeseq'] = form.cleaned_data['merged_seqs'].file.name
            anacapa_dict['reverseseq'] = form.cleaned_data['reverse_seqs'].file.name
            anacapa_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
            anacapa_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
            anacapa_dict['msa_phylo'] = form.cleaned_data['msa_phylo']
            call_course_wrapper('Anacapa', anacapa_dict, anacapa_metadata_dict)
            return redirect('/output/')
        else:
            context['errors'] = form.errors
    else:
        context['form'] = AnacapaForm()
    return render(request, 'anacapa.html', context)


def output_view(request):
    context = {}
    context['list'] = [i for i in os.listdir('output') if i != '.DS_Store']
    return render(request, 'output.html', context)


def mrdna(request):
    context = {}
    context['form'] = MrDNAForm()
    if request.method == 'POST':
        form = MrDNAForm(request.POST, request.FILES)
        if form.is_valid():
            mrdna_dict = files_dictionary
            mrdna_metadata_dict = metadata_dictionary
            mrdna_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
            mrdna_dict['otutable'] = form.cleaned_data['otu_table'].file.name
            mrdna_dict['fwdseq'] = form.cleaned_data['all_seqs'].file.name
            mrdna_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
            mrdna_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
            mrdna_dict['msa_phylo'] = form.cleaned_data['msa_phylo']
            call_course_wrapper('MrDNA', mrdna_dict, mrdna_metadata_dict)
            return redirect('/output/')
        else:
            context['errors'] = form.errors
    else:
        context['form'] = MrDNAForm()
    return render(request, 'mrdna.html', context)


def qiime2(request):
    context = {}
    context['form'] = QIIME2Form()
    if request.method == 'POST':
        form = QIIME2Form(request.POST, request.FILES)
        if form.is_valid():
            qiime2_dict = files_dictionary
            qiime2_metadata_dict = metadata_dictionary
            qiime2_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
            qiime2_dict['otutable'] = form.cleaned_data['otu_table'].file.name
            qiime2_dict['fwdseq'] = form.cleaned_data['all_seqs'].file.name
            qiime2_dict['taxonomy'] = form.cleaned_data['taxonomy'].file.name
            qiime2_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
            qiime2_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
            qiime2_dict['msa_phylo'] = form.cleaned_data['msa_phylo']
            QIIME2(qiime2_dict, qiime2_metadata_dict)
            return redirect('/output/')

        else:
            context['errors'] = form.errors
    else:
        context['form'] = QIIME2Form()
    return render(request, 'qiime2.html', context)


def piphillin(request, num):
    context = {}
    context['number'] = num
    context['form'] = PiphillinForm(number_forms=num)
    if request.method == 'POST':
        # form = PiphillinForm(request.FILES, number_forms=num)
        # if form.is_valid():
        master_string = ''
        for i in range(1, num+1):
            file = request.FILES['zip_file_%s' % str(i)].file.name
            if i == num:
                master_string += file
            else:
                master_string += file + ','
        verified_metadata = request.FILES['verified_metadata']
        os.system('python puma/pumagui/functional_profile.py -i %s -o testing -metadata %s' % (master_string, verified_metadata))
        return redirect('/output/')

    else:
        context['form'] = PiphillinForm(number_forms=num)
    return render(request, 'piphillin.html', context)

def display_log(request, directory):
    context = {}
    context['file'] = []
    file = open("output/%s/log.txt" % directory)
    for line in file:
        context['file'].append(line)
    return render(request, 'log_output.html', context)


def get_output(request, directory):
    """
    A django view to zip files in directory and send it as downloadable response to the browser.
    Args:
      @request: Django request object
      @file_name: Name of the directory to be zipped
    Returns:
      A downloadable Http response
    """
    file_name = directory
    files_path = "output/%s" % directory
    path_to_zip = make_archive(files_path, "zip", files_path)
    response = HttpResponse(FileWrapper(open(path_to_zip,'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="{filename}.zip"'.format(
        filename = file_name.replace(" ", "_")
    )
    return response