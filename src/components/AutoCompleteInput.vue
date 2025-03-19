<template>
    <div class="autocomplete">
      <input 
        type="text" 
        v-model="inputValue"
        @input="filterOptions"
        @blur="hideDropdown"
        @focus="showDropdown = true"
        placeholder="이름을 입력하세요"
      />
      <ul v-if="showDropdown && filteredOptions.length">
        <li v-for="option in filteredOptions" :key="option" @click="selectOption(option)">
          {{ option }}
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  
  const props = defineProps(["options"]);
  const emit = defineEmits(["update:modelValue"]);
  
  const inputValue = ref("");
  const showDropdown = ref(false);
  const filteredOptions = ref([]);
  
  const filterOptions = () => {
    filteredOptions.value = props.options.filter(option =>
      option.toLowerCase().includes(inputValue.value.toLowerCase())
    );
  };
  
  const selectOption = (option) => {
    inputValue.value = option;
    emit("update:modelValue", option);
    showDropdown.value = false;
  };
  
  const hideDropdown = () => {
    setTimeout(() => {
      showDropdown.value = false;
    }, 200);
  };
  </script>
  
  <style scoped>
  .autocomplete {
    position: relative;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
  }
  
  ul {
    list-style: none;
    padding: 0;
    border: 1px solid #ccc;
    background: white;
    position: absolute;
    width: 100%;
    z-index: 10;
  }
  
  li {
    padding: 8px;
    cursor: pointer;
  }
  
  li:hover {
    background: #f0f0f0;
  }
  </style>
  