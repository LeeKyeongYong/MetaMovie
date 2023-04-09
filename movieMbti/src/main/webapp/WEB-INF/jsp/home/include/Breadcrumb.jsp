<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions"%>
 <a href="animeDetails.do?movie_seq=${movies.movie_seq}">
<section class="normal-breadcrumb set-bg" data-setbg="${imgUrl}/${movies.movie_img}.jpg">
      <div class="container">
            <div class="row">
                <div class="col-lg-12 text-center">
                    <div class="normal__breadcrumb__text_login">
                       
                          <h2>${movies.movie_title}</h2>
                           <p>${fn:substring(movies.movie_content,0,26)}&nbsp;....</p>
                       
                    </div>
                </div>
            </div>
        </div>
</section>
 </a> 