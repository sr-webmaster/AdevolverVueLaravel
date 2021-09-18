import Accounts from "./components/accounts/Accounts";
import { AlertPlugin } from 'bootstrap-vue'
import App from "./views/App.vue";
import BudgetCommander from "./components/budget-commander/BudgetCommander.vue"
import Feed from './components/feed/Feed.vue'
import Vue from 'vue'
import Vue2Filters from 'vue2-filters'
import VueCurrencyInput from 'vue-currency-input'
import VueInputAutowidth from 'vue-input-autowidth'
import routes from "./routes";
import store from './store'

// import Vuetify from 'vuetify'
// import 'vuetify/dist/vuetify.min.css'
// import vuetify from '@/plugins/vuetify' // path to vuetify export

Vue.use(AlertPlugin)
Vue.use(VueInputAutowidth)
Vue.use(VueCurrencyInput)
Vue.use(Vue2Filters)
window.Event = new Vue();
Vue.use(require('vue-resource'));
Vue.use(require('bootstrap-vue'));

// Vue.use(Vuetify)

// const opts = {}

// export default new Vuetify(opts)


try{
  Vue.prototype.$userId = document.querySelector("meta[name='user-id']").getAttribute('content');
}catch{
  Vue.prototype.$userId = ''
}

try{
  Vue.prototype.$userImageUrl = document.querySelector("meta[name='user-img-url']").getAttribute('content');
}catch{
  Vue.prototype.$userImageUrl = ''
}

//the account id meta might not be defined
try{
  Vue.prototype.$accountId = document.querySelector("meta[name='account-id']").getAttribute('content');
}catch{
  Vue.prototype.$accountId = ''
}

Vue.component('InfiniteLoading', require('vue-infinite-loading'));
Vue.component('feed', require('./components/feed/Feed.vue'));
Vue.component('notifications', require('./components/common/notifications/Notifications.vue'));
// Vue.component('budget-commander', require('../../js/components/budget-commander/BudgetCommander.vue'));
// Vue.component('ad-test', require('../../js/components/ad-test/AdTest.vue'));

new Vue({
  store,
  el: "#app",
  router: routes,
  components: {
    App,
    Feed,
    BudgetCommander,
    Accounts,
  }
})