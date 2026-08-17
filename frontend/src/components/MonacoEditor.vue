<template>
	<div class="monaco-wrapper">
		<div ref="editorContainer" class="monaco-editor"></div>
	</div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as monaco from 'monaco-editor'

const props = defineProps({
	modelValue: {
		type: String,
		default: '',
	},
	language: {
		type: String,
		default: 'cpp',
	},
})

const emit = defineEmits(['update:modelValue'])

const editorContainer = ref(null)
let editor = null

onMounted(() => {
	editor = monaco.editor.create(editorContainer.value, {
		value: props.modelValue,
		language: props.language,

		theme: 'vs-dark',

		automaticLayout: true,

		minimap: {
			enabled: false,
		},

		fontSize: 14,

		lineNumbers: 'on',

		scrollBeyondLastLine: false,

		padding: {
			top: 12,
			bottom: 12,
		},
	})

	editor.onDidChangeModelContent(() => {
		emit('update:modelValue', editor.getValue())
	})
})

watch(
	() => props.modelValue,
	(value) => {
		if (editor && value !== editor.getValue()) {
			editor.setValue(value)
		}
	}
)

watch(
	() => props.language,
	(language) => {
		if (!editor) return

		const model = editor.getModel()

		if (model) {
			monaco.editor.setModelLanguage(model, language)
		}
	}
)

onBeforeUnmount(() => {
	if (editor) {
		editor.dispose()
		editor = null
	}
})
</script>

<style scoped>
.monaco-wrapper {
	width: 100%;
	height: 100%;
	min-height: 700px;
	border-radius: 8px;
	overflow: hidden;
	border: 1px solid var(--outline-gray-2);
}

.monaco-editor {
	width: 100%;
	height: 100%;
}
</style>
