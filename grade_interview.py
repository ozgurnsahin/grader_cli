from llm_functions import ChatbotFunctions
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Grade interview transcripts using AI against a provided rubric",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    parser.add_argument(
        '--rubric', '-r',
        type=str,
        required=True,
        help='Path to the rubric JSON file'
    )
    
    parser.add_argument(
        '--transcript', '-t', 
        type=str,
        required=True,
        help='Path to the interview transcript text file'
    )

    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Path where the analysis JSON will be written'
    )
    
    return parser.parse_args()

def main():
    try:
        args = parse_arguments()
        grader = ChatbotFunctions()
    
        analysis = grader.grade_interview(
            rubric_file_path=args.rubric,
            transcript_file_path=args.transcript
        )
        grader.save_analysis(analysis, args.output)
    
    except Exception as e:
        print(f"\n Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()