document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'bar', // Standard bar chart

        // The data for our dataset
        data: {
            labels: ["TheBloke_Mixtral-8x7B-v0.1-GGUF", "NousResearch_Nous-Hermes-2-Yi-34B-GGUF", "TheBloke_Mixtral-8x7B-Instruct-v0.1-GGUF", "MaziyarPanahi_Mixtral-8x22B-v0.1-GGUF", "MaziyarPanahi_zephyr-orpo-141b-A35b-v0.1-GGUF", "TheBloke_orca_mini_v3_7B-GGUF", "MaziyarPanahi_gemma-7b-GGUF", "microsoft_Phi-3-mini-4k-instruct-gguf", "ggerganov_gemma-2b-Q8_0-GGUF", "microsoft_Phi-3-mini-4k-instruct-gguf", "xtuner_llava-phi-3-mini-gguf", "MaziyarPanahi_WizardLM-2-8x22B-GGUF", "dranger003_c4ai-command-r-plus-iMat.GGUF", "xtuner_llava-phi-3-mini-gguf", "TheBloke_TinyLlama-1.1B-1T-OpenOrca-GGUF", "QuantFactory_Meta-Llama-3-8B-GGUF", "MaziyarPanahi_Meta-Llama-3-70B-Instruct-GGUF", "SanctumAI_Meta-Llama-3-8B-Instruct-GGUF", "dranger003_Qwen1.5-72B-Chat-iMat.GGUF", "TheBloke_TinyLlama-1.1B-Chat-v1.0-GGUF", "bartowski_Qwen1.5-110B-Chat-GGUF", "cloudyu_Yi-34Bx2-MoE-60B-GGUF", "lmstudio-ai_gemma-2b-it-GGUF", "TheBloke_stablelm-zephyr-3b-GGUF", "brittlewis12_gemma-7b-it-GGUF"],
            datasets: [{
                label: 'PPL',
                backgroundColor: 'rgb(75, 192, 192)',
                borderColor: 'rgb(75, 192, 192)',
                data: [3.9198599999999995, 4.091008, 4.299140000000001, 5.033964, 5.050327999999999, 5.3757719999999996, 5.436572000000001, 6.251595999999999, 6.323403999999999, 6.40858, 6.699972, 6.8622320000000006, 6.882568, 6.893160000000002, 8.8118, 9.157792, 10.938352, 11.175504, 11.792568000000003, 12.023712000000003, 13.762304000000004, 15.985552, 16.311272, 22.694716, 23.653612000000003],
            }]
        },

        // Configuration options go here
        options: {
            indexAxis: 'y', // Set the horizontal orientation by specifying y-axis as the index axis
            scales: {
                x: { // Adjusted for version 3, x axis is now 'x' not 'xAxes'
                    type: 'logarithmic',
                    position: 'bottom',
                    ticks: {
                        min: 1, // Minimum value for the x-axis
                        max: 30, // Maximum value you expect for the x-axis
                        callback: function(value, index, values) {
                            return Number(value.toString()); // Needed to format ticks correctly for logarithmic scale
                        }
                    }
                }
            },
            maintainAspectRatio: false // Ensures that the chart does not distort on different screens
        }
    });
});

