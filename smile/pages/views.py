from django.shortcuts import render

def black_page(request):
    context = {
        'profile': {
            'name': 'nenekawaiiii',
            'bio': '旅行的意义在于发现自我。',
            'status': {
                'name': 's1osomeone',
                'last_seen': '9 minutes ago'
            },
            'views': 1128
        }
    }
    return render(request, 'pages/black.html', context)