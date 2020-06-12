import Vue from 'vue';
import VueRouter from 'vue-router';
import MainMap from '../components/mainMap/MainMap.vue';
import MovieDetail from '../components/movieDetail/MovieDetail.vue';
import Search from '../components/search/Search.vue';
import Signup from '../components/signup/Signup.vue';
import UserPage from '../components/userPage/UserPage.vue';
import FirstRating from '../components/firstRating/FirstRating.vue';
import CinemaDetail from '../components/cinemaDetail/CinemaDetail';
import NotFound from '../components/notFound/NotFound';


Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'MainMap',
    component: MainMap
  },
  {
    path: '/movie/:id',
    name: 'MovieDetail',
    component: MovieDetail
  },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  {
    path: '/userPage',
    name: 'UserPage',
    component: UserPage
  },
  {
    path: '/firstRating',
    name: 'FirstRating',
    component: FirstRating
  },
  {
    path: '/cinema/:id',
    name: 'CinemaDetail',
    component: CinemaDetail
  },
  {
    path: '/404',
    name: 'NotFound', 
    component: NotFound
  },
  {
    path: '*',
    redirect: '/404',
  },
  
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } 
    if (to.hash) {
      return { selector: to.hash };
    }
    return { x: 0, y: 0 };
  },
});


export default router;
