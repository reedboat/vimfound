<!doctype html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>vim plugins</title>
        <link href="/css/bootstrap.min.css" rel="stylesheet" media="screen"/>
        <style> body { padding-top: 60px;}</style>
        <link href="/css/bootstrap-responsive.css" rel="stylesheet" />
        <link href="/img/favicon.ico" rel="shortcut icon" />
        <script>
            window.onload = function(){
                elems = document.getElementsByTagName("select");
                elems[0].value ='{{type}}'
                elems[1].value ='{{sort}}'
                elems[2].value ='{{year}}'
            }
        </script>
    </head>
    <body>
        <div class="navbar navbar-fixed-top">
          <div class="navbar-inner">
            <div class="container">
              <a class="btn btn-navbar" data-target=".nav-collapse" data-toggle="collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </a>
              <a class="brand" href="#">Store</a>
              <div class="container nav-collapse">
                <ul class="nav">
                  <li><%= link_to "Link1", "/path1"  %></li>
                  <li><%= link_to "Link2", "/path2"  %></li>
                  <li><%= link_to "Link3", "/path3"  %></li>
                </ul>
              </div><!--/.nav-collapse -->
            </div>
          </div>
        </div>
        <div class="container">
            <div class="row">
                <div class="span9">
                    <div class="page-header">
                        <h1>vim插件查询</h1>
                    </div>
                    <form action="" method="get" class="form">
                        <div>
                        <label>查询:</label><input name="keyword" type="text" value="" />
                        </div>
                        <div>
                            <label>插件类型:</label>
                            <select name="type" value="{{type}}">
                                <option value="all">all</option>
                                <option value="utility">utility</option>
                                <option value="ftplugin">ftplugin</option>
                                <option value="indent">indent</option>
                                <option value="color scheme">color scheme</option>
                            </select>
                        </div>
                        <div>
                            <label>排序方式</label>
                            <select name="sort" value="{{sort}}">
                                <option value="score">score</option>
                                <option value="ratings">ratings</option>
                                <option value="downloads">downloads</option>
                            </select>
                        </div>
                        <div>
                            <label>时间：</label>
                            <select name="year" value="{{year}}">
                                <option value="1">1年内</option>
                                <option value="2">2年内</option>
                                <option value="3">3年内</option>
                                <option value="4">4年内</option>
                                <option value="5">5年内</option>
                                <option value="0">全部</option>
                            </select>
                        </div>
                        <div>
                            <button type="submit" class="btn btn-primary">查询</button>
                        </div>
                    </form>
                    <table class="table table-stripped">
                        <thead>
                            <tr>
                            <th>index</th><th>name</th><th>type</th>
                            <th><a href="?sort=score">score</a></th>
                            <th><a href="?sort=ratings">ratings</a></th>
                            <th><a href="?sort=downloads">downloads</a></th>
                            <th>create_date</th><th>update date</th><th>desc</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for plugin in rows %}
                                <tr>
                                    <td>{{loop.index}}</td>
                                    <td><a target="_blank" href="http://www.vim.org/scripts/script.php?script_id={{plugin.id}}">{{plugin.name}}</a></td>
                                    <td>{{plugin.type}}</td>
                                    <td>{{"%.2f"|format(plugin.score)}}</td>
                                    <td>{{plugin.ratings}}/{{plugin.ratings_count}}</td>
                                    <td>{{plugin.downloads}}</td>
                                    <td>{{plugin.create_date}}</td>
                                    <td>{{plugin.update_date}}</td>
                                    <td>{{plugin.desc}}</td>
                                </tr> 
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                <div class="span3">
                    <div class="well sidebar-nav">
                        <h3></h3>
                        <div class="nav nav-list"></div>
                    </div>
                </div>
            </div>
        </div>
        <script type="text/javascript" src="/js/bootstrap.min.js"></script>
    </body>
</html>
