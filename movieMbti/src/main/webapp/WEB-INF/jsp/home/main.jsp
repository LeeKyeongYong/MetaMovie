<%--
  Created by IntelliJ IDEA.
  User: sleek
  Date: 2023-04-09
  Time: 오후 3:14
  To change this template use File | Settings | File Templates.
--%>
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
    <link rel="stylesheet" href="css/bootstrap.min.css" type="text/css">
    <link rel="stylesheet" href="css/font-awesome.min.css" type="text/css">
    <link rel="stylesheet" href="css/elegant-icons.css" type="text/css">
    <link rel="stylesheet" href="css/plyr.css" type="text/css">
    <link rel="stylesheet" href="css/nice-select.css" type="text/css">
    <link rel="stylesheet" href="css/owl.carousel.min.css" type="text/css">
    <link rel="stylesheet" href="css/slicknav.min.css" type="text/css">
    <link rel="stylesheet" href="css/style.css" type="text/css">
</head>

<body>
<!-- Page Preloder -->
<div id="preloder">
    <div class="loader"></div>
</div>
<!-- header -->
<%@ include file="./header.jsp"%>
<!-- Hero Section Begin -->
<section class="hero">
    <div class="container">
        <div class="hero__slider owl-carousel">

            <c:forEach items="${list1}" var="movies" varStatus="i" begin="0" end="2" step="1">
                <div class="hero__items set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
                    <div class="row">
                        <div class="col-lg-6">
                            <div class="hero__text">
                                <div class="label">${movies.movie_type}</div>
                                <h2>${movies.movie_title}</h2>
                                <p></p>
                                <a onclick="seqClick(${movies.movie_seq})" href="#Redirect"><span>Watch Now</span> <i class="fa fa-angle-right"></i></a>
                            </div>
                        </div>
                    </div>
                </div>
            </c:forEach>

        </div>
    </div>
</section>
<!-- Hero Section End -->

<!-- Product Section Begin -->
<section class="product spad">
    <div class="container">
        <div class="row">
            <div class="col-lg-8">
                <div class="trending__product">
                    <div class="row">
                        <div class="col-lg-8 col-md-8 col-sm-8">
                            <div class="section-title">
                                <h4>VOD 추천</h4>
                            </div>
                        </div>
                        <div class="col-lg-4 col-md-4 col-sm-4">
                            <div class="btn__all">
                                <a href="categories.do" class="primary-btn">View All <span class="arrow_right"></span></a>
                            </div>
                        </div>
                    </div>
                    <div class="row">

                        <c:forEach items="${list}" var="movies">
                            <div class="col-lg-4 col-md-6 col-sm-6">
                                <div style="cursor: pointer;" onclick="location.href='animeDetails.do?movie_seq=${movies.movie_seq}';">
                                    <div class="product__item">
                                        <div class="product__item__pic set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
                                            <div class="comment"><i class="fa fa-comments"></i>&nbsp; ${movies.cmt_seq}</div>
                                            <div class="view"><i class="fa fa-star"></i> ${movies.movie_rating/2}</div>
                                        </div>
                                        <div class="product__item__text">
                                            <ul>
                                                <li>Movie</li>
                                            </ul>
                                            <h5><a onclick="seqClick(${movies.movie_seq})" href="#Redirect">${movies.movie_title}</a></h5>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </c:forEach>

                    </div>
                </div>
            </div>
            <div class="col-lg-4 col-md-6 col-sm-8">
                <div class="product__sidebar">
                    <div class="product__sidebar__view">
                        <div class="section-title">
                            <h5>시청목록</h5></div>
                        <c:forEach items="${history_seq}" var="movies" varStatus="i">
                            <div class="filter__gallery">
                                <a onclick="seqClick(${movies.movie_seq})" href="#Redirect">
                                    <div class="product__sidebar__view__item set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
                                        <div class="view"><!-- <i class="fa fa-eye"> </i> 9141--></div>
                                        <h5 class="movie_gotitle">${movies.movie_title}</h5>
                                    </div>
                                </a>
                            </div>
                        </c:forEach>
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
<script src="js/jquery-3.3.1.min.js"></script>
<script src="js/bootstrap.min.js"></script>
<script src="js/player.js"></script>
<script src="js/jquery.nice-select.min.js"></script>
<script src="js/mixitup.min.js"></script>
<script src="js/jquery.slicknav.js"></script>
<script src="js/owl.carousel.min.js"></script>
<script src="js/main.js"></script>
<script type="text/javascript">
    /* 클릭시 flask로 movie_seq 값 전송 */
    function seqClick(seq) {
        console.log(seq)
        $.ajax({
            type : "post",
            url : "http://127.0.0.1:5000/recom_vod",
            data : JSON.stringify({"movie_seq":seq}),
            dataType: "JSON",
            contentType: "application/json; charset=utf-8",
            timeout: 4000,
            success : recomVod,
            error : function(e){
                console.log(e);
            }
        });
        /* 성공시 컨트롤러로 movie_seq 값(array) 이동 */
        function recomVod(data) {
            console.log(data)
            $.ajax({

                url : "recomVod.do",
                type : "POST",
                data : data,
                success : recom,
                error : recom
            });
        };
        /* 성공시 get방식  이동 */
        function recom() {
            location.href = "animeDetails.do?movie_seq="+seq;
        };
    }

</script>
<style>
    .movie_gotitle {
        color: #4641D9;
        font-weight: 700;
        line-height: 26px;
    }

    a:hover,
    a:focus {
        text-decoration: none;
        outline: none;
        color: #4641D9;
    }
</style>
</body>

</html>