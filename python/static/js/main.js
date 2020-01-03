// 输出文件图标
function getType(type) {
    var result = "";
    if ((/excel/i).test(type)) type = 'xls';
    else if ((/zip/i).test(type)) type = 'zip';
    else if ((/word/i).test(type)) type = 'doc';
    else if ((/pdf/i).test(type)) type = 'pdf';
    else if ((/ppt/i).test(type)) type = 'ppt';
    else if ((/text/i).test(type)) type = 'txt';
    else if ((/png/i).test(type)) type = 'png';
    else if ((/jpeg/i).test(type)) type = 'jpeg';
    else if ((/audio/i).test(type)) type = 'mp3';
    else if ((/media/i).test(type)) type = 'mp4';

    switch (type) {
        case "zip": case "rar": case "7z":
            result = "file_zip";
            break;
        case "jpg": case "png": case "bmp": case "gif": case "ico":
            result = "file_img";
            break;
        case "htm": case "html":
            result = "file_html";
            break;
        case "php": case "css": case "jsp": case "js":
            result = "file_code";
            break;
        case "exe":
            result = "file_exe";
            break;
        case "docx": case "doc":
            result = "file_word";
            break;
        case "xlsx": case "xls":
            result = "file_excel";
            break;
        case "pptx": case "ppt":
            result = "file_ppt";
            break;
        case "pdf":
            result = "file_pdf";
            break;
        case "psd":
            result = "file_psd";
            break;
        case "mp4":
            result = "file_video";
            break;
        case "mp3":
            result = "file_music";
            break;
        case "txt":
            result = "file_txt";
            break;
        case "wjj":
            result = "folder";
            break;
        case "apk":
            result = "file_apk";
            break;
        default:
            result = "file";
    }
    return result;
}

var dir = '';
// 获取文件和目录
function getList(type, ListNav, ojb) {
    var root = '/home';
    var x=  document.getElementById("filename")
    $('#uploaddir').attr('action', '/upload&' + dir + '&' + x.value)
    dir = root + window.location.pathname + '/';
    switch (type) {
        case 'nav': case 'hash':
            dir = ListNav;
            break;
        case 'ml':
            dir = ListNav + $(ojb).text() + '/';
            break;
        default:
            var nav = '<a class="breadcrumb-item"></a>'
            $('#nav').html(nav);
    }
    $.ajax({
        url:'/getlist',
        type: 'POST',
        data: { 'dir': dir.valueOf() },
        dataType: 'json',
        error: function () {
            $('#list').html('<th class="text-center" colspan="4">请求错误</th>');
        },
        success: function (data) {
            setHash(dir);// 设置hash
            var str = '';
            var item = data;
            var keys = Object.keys(item)
            for (var i = 0; i < keys.length; i++) {
                if (item[i].type == 'directory') {
                    var name = '<a href="javascript:;" onclick="getList(\'ml\',\'' + dir + '\',this)">' + item[i].name + '</a>';
                } else {
                    // var name = '<a href = "file:///home/edxuanlen/Documents/'+ item[i].name + '" Preview(\'' + item[i].type + '\',\'' + item[i].name + '\', \'' + dir + item[i].name + '\')">' + item[i].name ;
                    var name = '<a href="javascript:;" onclick="Preview(\'' + item[i].type + '\',\'' + item[i].name + '\', \'' + dir + item[i].name + '\')">' + item[i].name + '</a>';
                }

                var x=  document.getElementById("filename")
                $('#uploaddir').attr('action', '/upload&' + dir + '&' + x.value)

                str += '<tr><td><svg class="icon" aria-hidden="true"><use xlink:href="#icon-' + getType(item[i].type) + '"></use></svg></td><td>' + name + '</td><td class ="text-right">' + item[i].size + '</td><td class ="text-center">' + item[i].time + '</td></tr>';
            }
            switch (type) {
                case 'nav':
                    $(ojb).nextAll().detach();
                    break;
                case 'ml':
                    var nav = '<a  class="breadcrumb-item" href="javascript:;"  onclick="getList(\'nav\',\'' + dir + '\',this)">' + $(ojb).text() + '</a>';
                    $('#nav').append(nav);
                    break;
                case 'hash':
                    var nav = '<a class="breadcrumb-item"></a>',
                        dir2 = '',
                        arr = dir.split('/'),
                        Max = arr.length - 1;
                    for (var i = 0; i < Max; i++) {
                        dir2 += arr[i] + '/';
                        nav += '<a  class="breadcrumb-item" href="javascript:;"  onclick="getList(\'nav\',\'' + dir2 + '\',this)">' + arr[i] + '</a>';
                    }
                    $('#nav').html(nav);
                    break;
            }
            $('#list').html(str);
        }
    });
}

function getDir() {
    var x=  document.getElementById("filename");
    $('#uploaddir').attr('action', '/upload&' + dir + '&' + x.value)
}

// 下载、预览文件
function Preview(type, title, dir, gtData = {}) {
    window.location.href=dir
}


// 设置hash
function setHash(dir) {
    location.hash = '/' + dir;
    nowHash = dir;
}
// 监控hash
function doHash() {
    if (location.hash.substr(-1) != '/') {
        getList();
        return;
    }
    var hash = decodeURI(location.hash.replace('#/', ''));
    if (hash != nowHash) {
        getList('hash', hash);
    }
}