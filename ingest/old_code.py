class IngestView(View):
    model = Upload
    form = UploadForm

    def get(self, request, *args, **kwargs):
        return render(request, 'ingest/upload.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            # get the uploaded file
            file = request.FILES['content']
            # file information
            context = dict()
            context['name'] = file.name
            context['size'] = file.size
            context['content_type'] = file.content_type

            # save uploaded file
            obj = Upload.objects.create(title=request.POST['title'], uploaded_file=file)
            context['url'] = obj.uploaded_file.url
            context['title'] = obj.title
            obj.save()
            return render(request, 'ingest/uploaded.html', {'context': context})
        else:
            error = 'please check your data'

        return render(request, 'ingest/upload.html', {'form': self.form, 'error': error})