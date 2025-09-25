"""
媒体文件CORS中间件
解决前端跨域访问媒体文件的问题
"""

class MediaCORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # 如果是媒体文件请求，添加CORS头部
        if request.path.startswith('/media/'):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type'
            response['Access-Control-Max-Age'] = '86400'
            
        return response