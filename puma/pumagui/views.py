import os
import zipfile
# import StringIO

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import redirect
from .forms import *
from .templates import *
from .course_wrapper import *

files_dictionary = {"otutable": '', "fwdseq": '', "reverseseq": '', "mergeseq": '', "unique_id": '',
                    "allseqs": '', "taxonomy": '', "rarefactiondepth": 0, "rarefactioniter": 0,
                    "msa_phylo": True, "outdir": ''}

metadata_dictionary = {"metadata": ''}


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
            Anacapa(anacapa_dict, anacapa_metadata_dict)
            return redirect('/output/')
        else:
            context['errors'] = form.errors
    else:
        context['form'] = AnacapaForm()
    return render(request, 'anacapa.html', context)


def output_view(request):
    context = {}
    context['list'] = [i for i in os.listdir('output')]
    return render(request, 'output.html', context)


def mrdna(request):
    context = {}
    context['form'] = MrDNAForm()
    if request.method == 'POST':
        form = MrDNAForm(request.POST, request.FILES)
        if form.is_valid():
            anacapa_dict = files_dictionary
            anacapa_metadata_dict = metadata_dictionary
            anacapa_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
            anacapa_dict['otutable'] = form.cleaned_data['otu_table'].file.name
            anacapa_dict['fwdseq'] = form.cleaned_data['all_seqs'].file.name
            anacapa_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
            anacapa_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
            MrDNA(anacapa_dict, anacapa_metadata_dict)
            return redirect()
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
            anacapa_dict = files_dictionary
            anacapa_metadata_dict = metadata_dictionary
            anacapa_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
            anacapa_dict['otutable'] = form.cleaned_data['otu_table'].file.name
            anacapa_dict['fwdseq'] = form.cleaned_data['all_seqs'].file.name
            anacapa_dict['taxonomy'] = form.cleaned_data['taxonomy'].file.name
            anacapa_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
            anacapa_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
            QIIME2(anacapa_dict, anacapa_metadata_dict)

        else:
            context['errors'] = form.errors
    else:
        context['form'] = QIIME2Form()
    return render(request, 'qiime2.html', context)


# def piphillin(request):
#     context = {}
#     context['form'] = Form()
#     if request.method == 'POST':
#         form = AnacapaForm(request.POST, request.FILES)
#         if form.is_valid():
#             anacapa_dict = files_dictionary
#             anacapa_metadata_dict = metadata_dictionary
#             anacapa_metadata_dict['metadata'] = form.cleaned_data['metadata'].file.name
#             anacapa_dict['otutable'] = form.cleaned_data['otu_table'].file.name
#             anacapa_dict['fwdseq'] = form.cleaned_data['forward_seqs'].file.name
#             anacapa_dict['mergeseq'] = form.cleaned_data['merged_seqs'].file.name
#             anacapa_dict['reverseseq'] = form.cleaned_data['reverse_seqs'].file.name
#             anacapa_dict['rarefactiondepth'] = form.cleaned_data['rarefaction_depth']
#             anacapa_dict['rarefactioniter'] = form.cleaned_data['rarefaction_iterations']
#             Anacapa(anacapa_dict, anacapa_metadata_dict)
#
#         else:
#             context['errors'] = form.errors
#     else:
#         context['form'] = AnacapaForm()
#     return render(request, 'anacapa.html', context)


# def getfiles(request):
#     # Files (local path) to put in the .zip
#     # FIXME: Change this (get paths from DB etc)
#     filenames = ["/tmp/file1.txt", "/tmp/file2.txt"]
#
#     # Folder name in ZIP archive which contains the above files
#     # E.g [thearchive.zip]/somefiles/file2.txt
#     # FIXME: Set this to something better
#     zip_subdir = "somefiles"
#     zip_filename = "%s.zip" % zip_subdir
#
#     # Open StringIO to grab in-memory ZIP contents
#     s = StringIO.StringIO()
#
#     # The zip compressor
#     zf = zipfile.ZipFile(s, "w")
#
#     for fpath in filenames:
#         # Calculate path for file in zip
#         fdir, fname = os.path.split(fpath)
#         zip_path = os.path.join(zip_subdir, fname)
#
#         # Add file, at correct path
#         zf.write(fpath, zip_path)
#
#     # Must close zip for all contents to be written
#     zf.close()
#
#     # Grab ZIP file from in-memory, make response with correct MIME-type
#     resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
#     # ..and correct content-disposition
#     resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
#
#     return resp