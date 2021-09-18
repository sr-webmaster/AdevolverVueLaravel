<template>
  <div class="w-full" v-scroll="handleScroll">
    <main>

      <div class="py-2">
        <div class="flex flex-wrap justify-between">
          <div class="flex flex-wrap">
            <div class="flex mr-6">
              <div class="flex flex-wrap py-1 px-3 text-danger text-xl font-semibold"></div>
              <div class="flex">
                <div class="m-auto"></div>
              </div>
            </div>
          </div>
          <div class="pr-4">Last 30 days</div>
        </div>
      </div>

      <div class="py-2 flex content-end">  
        <Search
          placeholder="Search accounts.."
          @handleSearchInput="debounceSearch"
        />
      </div>

      <div class="py-2 content-end">
        <h2 style="text-align: center;font-weight: 700; font-size: large; width: 100%;">Early Access</h2>
        <p style="text-align: center;">Use the Sync toggle to activate an account. <i>Note 1 account is available during early access.</i></p>
      </div>
      
      <div class="py-2">
        <LoadingIndicator v-if="loading" />
        <AccountsList
          v-else
          :list='list'
          :searchKey='searchKey'
          :perPage='perPage'
        />
      </div>
    </main>
  </div>
</template>

<script>
import AccountsList from "./AccountsList.vue"
import { 
  mapState,
  mapActions, 
} from 'vuex'
import * as types from '@/store/modules/accounts/types'
import { debounce } from 'debounce'
import { DEBOUNCE } from '@/config/constants'
import { isBottom } from '@/helpers/helpers'
import LoadingIndicator from '@/components/common/LoadingIndicator.vue'
import Search from '@/components/common/Search.vue'
import _ from 'lodash'

export default {
  name: "Accounts",
  data () {
    return {
      user: this.$route.params.user_id,
      searchKey: '',
      perPage: 20,
    }
  },
  components: {
    AccountsList,
    LoadingIndicator,
    Search
  },
  directives: {
    scroll: {
      inserted: function(el, binding) {
        let f = function (evt) {
          if (binding.value(evt, el)) {
            window.removeEventListener('scroll', f)
          }
        }
        window.addEventListener('scroll', f)
      }
    }
  },
  created () {
    window.scrollTo(0, 0)
    if(this.list.length === 0) {
      this[types.GET_ACCOUNTS](this.user).then(res => {
        this[types.GET_CURRENCY](res[0].id)

        if(res.length < 20) {
          this.perPage = res.length
        }
      }, error => {
        console.error(error)
        if(error.response && error.response.status>=400){
          window.location.replace('/login');
        }
      })
    }

    this[types.GET_NUMBER_OF_SYNCED_ACCOUNTS](this.user).then(res => {

    }, error => {
      console.error(error)
    })

    let self = this
    this.debounceSearch = debounce( e => {
      self.searchKey = e.target.value
      self.perPage = self.list.length < 20 ? self.list.length : 20
    }, DEBOUNCE.DEFAULT)
  },
  
  methods:{
    ...mapActions('accounts', [
      types.GET_ACCOUNTS,
      types.GET_CURRENCY,
      types.GET_NUMBER_OF_SYNCED_ACCOUNTS,
    ]),
    handleScroll: function(evt) {
      if(isBottom()) {
        this.perPage + 20 < this.list.length ? this.perPage += 20 : this.perPage = this.list.length
      }
    }
  },

  computed:{
    ...mapState('accounts', {
      list: state => state.list,
      loading: state => state[`${_.camelCase(types.GET_ACCOUNTS)}Pending`]
    })
  },
}

</script>

<style scoped>

</style>