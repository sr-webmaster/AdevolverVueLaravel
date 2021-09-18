<template>
  <div>
    <div v-show="searchKey === ''">
      <AccountItem
        :key="account.id"
        :account="account"
        v-for="account in this.list.slice(0, perPage)"
      />
    </div>
    <div v-show="searchKey !== ''">
      <AccountItem
        :key="account.id"
        :account="account"
        v-for="account in filteredList.slice(0, perPage)"
      />
    </div>
  </div>
</template>

<script>
import * as types from '@/store/modules/accounts/types'
import AccountItem from './AccountItem'

export default {
  name: "AccountsList",
  props: {
    list: {
      type: Array,
      required: true
    },
    searchKey: {
      type: String,
      required: true
    },
    perPage: {
      type: Number,
      required: true
    }
  },
  components: {
    AccountItem
  }, 
  computed: {
    filteredList: function () {
      if(this.searchKey !== '') {
        return this.list.filter(account => {
          return account.name.toLowerCase().includes(this.searchKey.toLowerCase())
        })
      } else return []
    }
  }
}

</script>

<style scoped>

</style>