



def customCSS():
    custom_css = '''
            
        h2 {
            color: white;
        }

        .gradio-container {
            width: 1000px;
            margin: auto;
            padding: 20px;
            background: #343434;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        button {
            background: #f97316;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background: #b2560d;
        }


        .play-manually-btn {
            margin-right: 16px; /* Adjust the value as needed */
        }

        .button-group {
            display: flex;
            gap: 20px; /* Adjust the gap as needed */
        }
        
    '''   
    return custom_css