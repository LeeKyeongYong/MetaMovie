<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<c:set var ="imgUrl"><%="http://gjaischool-b.ddns.net:8086/crawlingImage"%></c:set>
<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="description" content="Anime Template">
    <meta name="keywords" content="Anime, unica, creative, html">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>NeTupidia</title>

    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Mulish:wght@300;400;500;600;700;800;900&display=swap"
    rel="stylesheet">

    <!-- Css Styles -->
    <link rel="stylesheet" href="resources/css/bootstrap.min.css" type="text/css">
    <link rel="stylesheet" href="resources/css/font-awesome.min.css" type="text/css">
    <link rel="stylesheet" href="resources/css/elegant-icons.css" type="text/css">
    <link rel="stylesheet" href="resources/css/plyr.css" type="text/css">
    <link rel="stylesheet" href="resources/css/nice-select.css" type="text/css">
    <link rel="stylesheet" href="resources/css/owl.carousel.min.css" type="text/css">
    <link rel="stylesheet" href="resources/css/slicknav.min.css" type="text/css">
    <link rel="stylesheet" href="resources/css/style.css" type="text/css">
</head>

<body>
    <!-- Page Preloder -->
    <div id="preloder">
        <div class="loader"></div>
    </div>

  <!-- header -->
	<%@ include file="./header.jsp"%>
    <!-- Breadcrumb Begin -->
    <div class="breadcrumb-option">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="breadcrumb__links">
                        <a href="index.do"><i class="fa fa-home"></i> Home</a>
                        <a href="categories.do">Categories</a>
                        <span>${param.movie_type}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Breadcrumb End -->

    <!-- Product Section Begin -->
    <section class="product-page spad">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <div class="product__page__content">
                        <div class="product__page__title">
                        </div>
                        <div class="row">
                        	<c:choose>
                        	<c:when test="${param.movie_type != null }">
                       		<c:forEach items="${typeList}" var="movies" varStatus="i" begin="${paging.firstRow}" end="${paging.lastRow}" step="1">
	                            <div class="col-lg-4 col-md-6 col-sm-6">
	                                <div class="product__item">
	                                    <div class="product__item__pic set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
	                                        <div class="comment"><i class="fa fa-comments"></i> 11</div>
	                                        <div class="view"><i class="fa fa-star"></i> ${movies.movie_rating/2}</div>
	                                    </div>
	                                    <div class="product__item__text">
	                                        <ul>
	                                            <li>Movie</li>
	                                        </ul>
	                                        <h5><a href="animeDetails.do?movie_seq=${movies.movie_seq}">${movies.movie_title}</a></h5>
	                                    </div>
	                                </div>
	                            </div>
                            </c:forEach>
                            </c:when>
                            <c:otherwise>
                            	<c:forEach items="${list}" var="movies" varStatus="i" begin="${paging.firstRow}" end="${paging.lastRow}" step="1">
	                            <div class="col-lg-4 col-md-6 col-sm-6">
	                                <div class="product__item">
	                                    <div class="product__item__pic set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
	                                        <div class="comment"><i class="fa fa-comments"></i> 11</div>
	                                        <div class="view"><i class="fa fa-star"></i> ${movies.movie_rating/2}</div>
	                                    </div>
	                                    <div class="product__item__text">
	                                        <ul>
	                                            <li>Movie</li>
	                                        </ul>
	                                        <h5><a href="animeDetails.do?movie_seq=${movies.movie_seq}">${movies.movie_title}</a></h5>
	                                    </div>
	                                </div>
	                            </div>
                            </c:forEach>
                            </c:otherwise>
                            </c:choose>
                        </div>
                    </div>
                    <div class="product__pagination">
                    	<c:choose>
                    	<c:when test="${param.movie_type != null}">
	                    	<a href="categories.do?movie_type=${param.movie_type}&curPage=1"><i class="fa fa-angle-double-left"></i></a>
	                    	<a href="categories.do?movie_type=${param.movie_type}&curPage=${paging.curPage-1 }"><i class="fa fa-angle-left"></i></a>
	                    	<c:forEach begin="${paging.firstPage}" end="${paging.lastPage}" var="i">
	                   			<c:if test="${i eq paging.curPage }"><a href="categories.do?movie_type=${param.movie_type}&curPage=${i}" class="current-page">${i}</a></c:if>
	                   			<c:if test="${i ne paging.curPage }"><a href="categories.do?movie_type=${param.movie_type}&curPage=${i}">${i }</a></c:if>
	                    	</c:forEach>
	                    	<a href="categories.do?movie_type=${param.movie_type}&curPage=${paging.curPage+1 }"><i class="fa fa-angle-right"></i></a>
	                    	<a href="categories.do?movie_type=${param.movie_type}&curPage=${paging.totalPageCount}"><i class="fa fa-angle-double-right"></i></a>
                    	</c:when>
                    	<c:otherwise>
	                    	<a href="categories.do?curPage=1"><i class="fa fa-angle-double-left"></i></a>
	                    	<a href="categories.do?curPage=${paging.curPage-1 }"><i class="fa fa-angle-left"></i></a>
	                    	<c:forEach begin="${paging.firstPage}" end="${paging.lastPage}" var="i">
	                   			<c:if test="${i eq paging.curPage }"><a href="categories.do?curPage=${i}" class="current-page">${i}</a></c:if>
	                   			<c:if test="${i ne paging.curPage }"><a href="categories.do?curPage=${i}">${i }</a></c:if>
	                    	</c:forEach>
	                    	<a href="categories.do?curPage=${paging.curPage+1 }"><i class="fa fa-angle-right"></i></a>
	                    	<a href="categories.do?curPage=${paging.totalPageCount}"><i class="fa fa-angle-double-right"></i></a>
                    	</c:otherwise>
                    	</c:choose>
                    </div>
                </div>
                <div class="col-lg-4 col-md-6 col-sm-8">
                    <div class="product__sidebar">
                        <div class="product__sidebar__view">
                            <div class="section-title">
                                <h5>시청목록</h5>
                            </div>
                            <c:forEach items="${history_seq}" var="movies" >
	                      	<div class="filter__gallery">
		                        <div class="product__sidebar__view__item set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
		                        <div class="view"><!-- <i class="fa fa-eye"> </i> 9141--></div>
		                        <h5><a href="animeDetails.do?movie_seq=${movies.movie_seq}">${movies.movie_title}</a></h5>
		                        </div>
	                        </div>
                      	    </c:forEach>
    </div>
    <div class="product__sidebar__comment">
    </div>
</div>
</div>
</div>
</div>
</section>
<!-- Product Section End -->

<!-- footer section -->
		<%@ include file="./footer.jsp"%>

  <!-- Search model Begin -->
  <%@ include file="./search.jsp"%>
<!-- Search model end -->

<!-- Js Plugins -->
<script src="resources/js/jquery-3.3.1.min.js"></script>
<script src="resources/js/bootstrap.min.js"></script>
<script src="resources/js/player.js"></script>
<script src="resources/js/jquery.nice-select.min.js"></script>
<script src="resources/js/mixitup.min.js"></script>
<script src="resources/js/jquery.slicknav.js"></script>
<script src="resources/js/owl.carousel.min.js"></script>
<script src="resources/js/main.js"></script>

</body>

</html>