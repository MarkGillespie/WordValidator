import Vue from "vue";
import VueRouter from "vue-router";

import App from "./App.vue";
import WordValidator from "./views/WordValidator.vue";
import Anagrammer from "./views/Anagrammer.vue";
import Wordle from "./views/Wordle.vue";
import PageNotFound from "./views/PageNotFound.vue";

Vue.config.productionTip = false;
Vue.use(VueRouter);

export const router = new VueRouter({
  routes: [
    { path: "/", component: WordValidator, props: true },
    { path: "/Anagrammer", component: Anagrammer, props: true },
    { path: "/Anagrammer/:queryWord", component: Anagrammer, props: true },
    { path: "/Games/W(o*)rdle", component: Wordle, props: true },
    /* must come after other paths */
    { path: "/:queryWord", component: WordValidator, props: true },
    { path: "*", component: PageNotFound, props: true },
  ],
});

new Vue({
  el: "#app",
  router,
  render: (h) => h(App),
});
