<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
<c:set var ="context"><%=request.getContextPath()%></c:set>
<c:set var ="memberProfile"><%="http://gjaischool-b.ddns.net:8086/memberProfile"%></c:set>
<c:set var ="imgUrl"><%="http://gjaischool-b.ddns.net:8086/crawlingImage"%></c:set>
<c:set var ="userPhoto"><%="resources/memberPhoto"%></c:set>
<!DOCTYPE html>
<html lang="ko">
<%@ include file="./include/head.jsp"%>
<body>
    <!-- Page Preloder -->
    <div id="preloder">
        <div class="loader"></div>
    </div>

  <!-- header -->
	<%@ include file="./header.jsp"%>
    <!-- Breadcrumb Begin -->
   <%@ include file="./include/BreadcrumbUpcomming.jsp"%> 
    <!-- Breadcrumb End -->

    <!-- Product Section Begin -->
    <section class="product-page spad">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <div class="product__page__content">
                        <div class="product__page__title">
                            <div class="row">
                                <div class="col-lg-12 col-md-12 col-sm-12">
                                    <div class="section-title">
                                        <h4>최신영화 예고편 보기</h4>
                                    </div>
                                </div>
                                <!-- 
                                <div class="col-lg-4 col-md-4 col-sm-6">
                                    <div class="product__page__filter">
                                        <p>날짜별 검색</p>
                                        <select>
                                            <option value="">A-Z</option>
                                            <option value="">1-10</option>
                                            <option value="">10-50</option>
                                        </select>
                                    </div>
                                </div> 
                                -->
                            </div>
                        </div>
                        
                        <div class="row" id="rowproduct"></div>
                        
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
<%@ include file="./include/jsscript.jsp"%>
<!-- Js Plugins -->
	<script>
	$( function() {
	 
		showList();
	
	 });
	function showList(){
		var key = "f9a5e15b3b0e1e90e656e39bf714f0a3";
		var api_key = "9d58f50eea3bc0cebe233c422bbef69e";
		const rowproduct = document.querySelector('#rowproduct');
        const searchUrl = "https://api.themoviedb.org/3/movie/upcoming?api_key="+api_key+"&language=ko-KR&region=KR";
        const base_url = "https://image.tmdb.org/t/p/w300/";
      
        
       
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function(){
        	 if(xhr.readyState == 4 && xhr.status == 200){
        		 var jsonObj = JSON.parse(xhr.response);
        		 const results = jsonObj['results'];
        		   results.forEach(element => {
        			
        			var poster_path = element['poster_path'];
	 			 	var cmt_seq = element['id'];
	 			 	var movie_title = element['title'];
	 			 	var vote_average = element['vote_average'];
	 			 	var release_date = element['release_date'];
	 			 	var output="<div class='product__item'>";
	 			 	
	 			 	
	 			 	
        		 	if(element['release_date'].substring(0,4) == '2022' ){ //2022년 기준
        		 		
        		 		var apiUrl = "http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key="+key+"&movieNm="+element['title']+"&itemPerPage=1";
        		 		
        		 		fetch(apiUrl).then(res => res.json()).then(function(res){
        		 			 	var movieList=res.movieListResult.movieList;
        		 			 	var movie_seq=movieList[0].movieCd;
        		 			 	const myDiv = document.createElement('div');
        		 			    myDiv.classList.add('col-lg-3');
        			        	myDiv.classList.add('col-md-5');
        			        	myDiv.classList.add('col-sm-5');
        		 			    output+= "<a href='RankingDetails.do?cmt_seq="+cmt_seq+"&movie_seq="+movie_seq+"&movie_title="+movie_title+"'>";
        			        	output+= "<div class='product__item__pic set-bg' data-setbg='"+base_url+poster_path+"' style='background-image: url("+(base_url+poster_path)+");'>";
        			        	output+="<div class='comment'><i class='fa fa-star'></i>&nbsp;&nbsp; "+vote_average;
        			        	output+="</div> <div class='view'><i class='fa fa-upload'></i>&nbsp;&nbsp;"+release_date+"</div></div>";
        			        	output+="<div class='product__item__text'> <h5>"+movie_title+"</a></h5></div>";
        			        	output+="</div>";
        			        	myDiv.innerHTML=output;
        			        	rowproduct.appendChild(myDiv);
        			        	console.log(myDiv);	 
        		 		}).catch(error => console.log(error));

        		 	}
        		 }); 
        	  }
        	}
        xhr.open('GET',searchUrl, true);
        xhr.send();
	}
	</script>
</body>

</html>