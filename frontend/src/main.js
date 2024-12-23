import { mount } from 'svelte';
import Router from './Routing.svelte';

const app = mount(Router, {
  target: document.getElementById('app'),
});

export default app;