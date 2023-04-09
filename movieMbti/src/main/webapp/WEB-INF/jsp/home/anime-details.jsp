<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<c:set var ="context"><%=request.getContextPath()%></c:set>
<c:set var ="memberProfile"><%="http://gjaischool-b.ddns.net:8086/memberProfile"%></c:set>
<c:set var ="imgUrl"><%="http://gjaischool-b.ddns.net:8086/crawlingImage"%></c:set>
<c:set var ="userPhoto"><%="resources/memberPhoto"%></c:set>


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
    <link rel="stylesheet" href="resources/css/font-awesome.min.css" type="text/css">
    <link rel="stylesheet" href="resources/css/bootstrap.min.css" type="text/css">
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
                        <a href="categories.do">영화</a>
                        <span>${movie.movie_title}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Breadcrumb End -->

    <!-- Anime Section Begin -->
    <section class="anime-details spad">
        <div class="container">
            <div class="anime__details__content">
                <div class="row">
                    <div class="col-lg-3">
                        <div class="anime__details__pic set-bg" data-setbg="${imgUrl}/${movie.movie_img}.jpg">
                            <div class="comment"><i class="fa fa-comments"></i>&nbsp;${CommentsCnt}</div>
                            <div class="view"><i class="fa fa-eye"></i>&nbsp;${movie.movie_cnt}</div>
                            
                        </div>
                    </div>
                    <div class="col-lg-9">
                        <div class="anime__details__text">
                            <div class="anime__details__title">
                                <h3>${movie.movie_title}</h3>
                            </div>
                            <div class="anime__details__rating">
                                <div class="rating">
                                      <c:choose>
									     <c:when test = "${movie.movie_rating/2 >= 5}">
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									     </c:when>
									     <c:when test = "${movie.movie_rating/2 >= 4}">
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									         
									     </c:when>
									     <c:when test = "${movie.movie_rating/2 >= 3}">
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									     </c:when>
									     <c:when test = "${movie.movie_rating/2 >= 2}">
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									     </c:when>
									     <c:when test = "${movie.movie_rating/2 >= 1}">
									           <a href="#"><i class="fa fa-star"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									     </c:when>
         								<c:otherwise>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
									           <a href="#"><i class="fa fa-star-o"></i></a>
         								</c:otherwise>
                                      </c:choose>
                                </div>
                                <span>${movie.movie_participate} Votes</span>
                            </div>
                            <p>${movie.movie_content}</p>
                            <div class="anime__details__widget">
                                <div class="row">
                                    <div class="col-lg-12 col-md-12">
                                        <ul>
                                            <li><span>영화 유형 :</span> ${movie.movie_type}</li>
                                            <li><span>영화감독:</span>${movie.movie_director}</li>
                                            <li><span>영화 개봉날짜:</span> ${fn:substring(movie.movie_open_date,0,10)}&nbsp;&nbsp;개봉</li>
                                            <li><span>영화 러닝타임:</span>${movie.movie_runtime}</li>
                                            <li><span>영화 출연배우:</span>${movie.movie_actor}</li>
                                            <%-- <li><span>영화 등급:</span>${movie.movie_age}</li> --%>
                                            <li><span>영화 제작 국가:</span>${movie.movie_country}</li>
                                            <li><span>영화 평점:</span>${movie.movie_rating}&nbsp; 점</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-8 col-md-8">
                        <div class="anime__details__review">
                        
                            <div class="section-title">
                                <h5>Reviews</h5>
                            </div>
                           <c:forEach items="${CommentList}" var="Comment"> 
                            <div class="anime__review__item">
                                <div class="anime__review__item__pic">
                                  	<c:choose>
									     <c:when test = "${Comment.mb_profile ne '' and Comment.mb_profile ne null}">
                                    		<img src="${userPhoto}/${Comment.mb_profile}" alt="${Comment.mb_name} ( ${Comment.mb_id} ) 님의사진">
                                    	</c:when>
                                    	<c:otherwise>
                                    		<img src="${memberProfile}/memberProfile.jpg" alt="${Comment.mb_name} ( ${Comment.mb_id} ) 님의사진">
                                    	</c:otherwise>
                                    </c:choose>
                                </div>
                                <div class="anime__review__item__text">
                               		<h6>${Comment.mb_name}&nbsp;(&nbsp;${Comment.mb_id}&nbsp;)<span>&nbsp;&nbsp;&nbsp;${Comment.cmt_date}</span></h6>
                                    <p>${Comment.cmt_content}</p>
                                </div>
                            </div>
                        </c:forEach>
                        </div>
                        <div class="anime__details__form">
                            <div class="section-title">
                                <h5>Your Comment</h5>
                            </div>
                            
							<!--  별점 기능 -->
						 	<div class="mb-3" name="myform" id="myform" >
								<fieldset>
									<input type="radio" name="reviewStar" value="5" id="rate1"><label
										for="rate1">★</label>
									<input type="radio" name="reviewStar" value="4" id="rate2"><label
										for="rate2">★</label>
									<input type="radio" name="reviewStar" value="3" id="rate3"><label
										for="rate3">★</label>
									<input type="radio" name="reviewStar" value="2" id="rate4"><label
										for="rate4">★</label>
									<input type="radio" name="reviewStar" value="1" id="rate5"><label
										for="rate5">★</label>
								</fieldset>
							</div>	
						
                            <form  action="CommentWrite.do" id="cmt" method="post" >
                            	<input type="hidden" name="mb_id" id="mb_id" value="${sessionScope.mb_id}">
                            	<input type="hidden" name="movie_seq" id="movie_seq" value="${movie.movie_seq}">
                                <textarea placeholder="Your Comment" name="cmt_content" id="cmt_content"></textarea>
                                <c:if test="${sessionScope.mb_id != null}">
                                	<button type="submit"><i class="fa fa-location-arrow"></i> Review</button>
                                </c:if>
                            </form>
                        </div>
                    </div>
                    <div class="col-lg-4 col-md-4">
                        <div class="anime__details__sidebar">
                            <div class="section-title">
                                <h5>you might like...</h5>
                            </div>
                            <c:forEach items="${list_genre}" var="movies">
                            <div class="product__sidebar__view__item set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
                                 <h5><a onclick="seqClick(${movies.movie_seq})" href="#Redirect">${movies.movie_title}</a></h5>
                            </div>
                            </c:forEach>
                        </div>
                    </div>
                </div>
            </div>
         </div>
        </section>
        <!-- Anime Section End -->
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

		<style>
		#myform fieldset{
	    display: inline-block;
	    direction: rtl;
	    border:0;
		}
		#myform fieldset legend{
		    text-align: right;
		}
		#myform input[type=radio]{
		    display: none;
		}
		#myform label{
		    font-size: 2em;
		    color: transparent;
		    text-shadow: 0 0 0 #f0f0f0;
		}
		#myform label:hover{
		    text-shadow: 0 0 0 rgba(250, 208, 0, 0.99);
		}
		#myform label:hover ~ label{
		    text-shadow: 0 0 0 rgba(250, 208, 0, 0.99);
		}
		#myform input[type=radio]:checked ~ label{
		    text-shadow: 0 0 0 rgba(250, 208, 0, 0.99);
		}
		</style>

		
	   <script type="text/javascript">
        $('#myform').on('click' ,function () {
         
          var movie_rating = $('input[name="reviewStar"]:checked').val();
          var movie_seq = $('#movie_seq').val();
        if(movie_rating !=null){ 
  		$.ajax({
			url : "/vod/animeDetail.do",
			method : "post",
			datatype :'json',
			data : {
			"movie_seq" : movie_seq,
			"movie_rating" : movie_rating
			},
			success : function(data){
				console.log('성공');
			},
			error : function(e){
				console.log(e);
			}
		});
        }});
        
        
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
    		
     		function recom() {
    			location.href = "animeDetails.do?movie_seq="+seq;
    		};
    	}

    </script>
    </body>

    </html>